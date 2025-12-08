"""
Bulk import/export service for internship offers.
Supports CSV and JSON formats.
"""
import csv
import json
import io
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import InternshipOffer
from hospitals.models import Hospital
from departments.models import Department


def parse_date(date_str):
    """Parse date from string (YYYY-MM-DD format)."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


def validate_offer_row(row, hospital, line_number):
    """Validate a single offer row."""
    errors = []
    
    required = ['title', 'start_date', 'end_date', 'slots']
    for field in required:
        if not row.get(field):
            errors.append(f"Line {line_number}: Missing required field '{field}'")
    
    try:
        slots = int(row.get('slots', 0))
        if slots < 1:
            errors.append(f"Line {line_number}: Slots must be at least 1")
    except ValueError:
        errors.append(f"Line {line_number}: Slots must be a number")
    
    try:
        start = parse_date(row.get('start_date'))
        end = parse_date(row.get('end_date'))
        if start and end and start > end:
            errors.append(f"Line {line_number}: Start date must be before end date")
    except ValidationError as e:
        errors.append(f"Line {line_number}: {str(e)}")
    
    return errors


def import_offers_csv(file_content, hospital, created_by):
    """
    Import offers from CSV content.
    
    Expected columns:
    - title (required)
    - description
    - department (name, will lookup or skip)
    - start_date (YYYY-MM-DD, required)
    - end_date (YYYY-MM-DD, required)
    - slots (required)
    - specialty
    - requirements
    
    Returns:
        dict: {success: int, errors: list, created_ids: list}
    """
    result = {'success': 0, 'errors': [], 'created_ids': []}
    
    try:
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8-sig')  # Handle BOM
        
        reader = csv.DictReader(io.StringIO(file_content))
        rows = list(reader)
        
        if not rows:
            result['errors'].append("CSV file is empty or has no data rows")
            return result
        
        all_errors = []
        for i, row in enumerate(rows, start=2):  # Start at 2 (header is 1)
            errors = validate_offer_row(row, hospital, i)
            all_errors.extend(errors)
        
        if all_errors:
            result['errors'] = all_errors
            return result
        
        with transaction.atomic():
            for i, row in enumerate(rows, start=2):
                department = None
                if row.get('department'):
                    department = Department.objects.filter(
                        name__iexact=row['department'].strip(),
                        hospital=hospital
                    ).first()
                
                offer = InternshipOffer.objects.create(
                    hospital=hospital,
                    department=department,
                    created_by=created_by,
                    title=row['title'].strip(),
                    description=row.get('description', '').strip(),
                    start_date=parse_date(row['start_date']),
                    end_date=parse_date(row['end_date']),
                    slots=int(row['slots']),
                    available_slots=int(row['slots']),
                    specialty=row.get('specialty', '').strip(),
                    requirements=row.get('requirements', '').strip(),
                    status='draft',
                    validation_status='pending'
                )
                result['created_ids'].append(offer.id)
                result['success'] += 1
        
    except Exception as e:
        result['errors'].append(f"Import failed: {str(e)}")
    
    return result


def import_offers_json(file_content, hospital, created_by):
    """
    Import offers from JSON content.
    
    Expected format:
    {
        "offers": [
            {
                "title": "...",
                "description": "...",
                "start_date": "YYYY-MM-DD",
                "end_date": "YYYY-MM-DD",
                "slots": 5,
                ...
            }
        ]
    }
    """
    result = {'success': 0, 'errors': [], 'created_ids': []}
    
    try:
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        
        data = json.loads(file_content)
        offers_data = data.get('offers', data if isinstance(data, list) else [])
        
        if not offers_data:
            result['errors'].append("No offers found in JSON")
            return result
        
        all_errors = []
        for i, row in enumerate(offers_data, start=1):
            errors = validate_offer_row(row, hospital, i)
            all_errors.extend(errors)
        
        if all_errors:
            result['errors'] = all_errors
            return result
        
        with transaction.atomic():
            for row in offers_data:
                department = None
                if row.get('department'):
                    department = Department.objects.filter(
                        name__iexact=row['department'],
                        hospital=hospital
                    ).first()
                
                offer = InternshipOffer.objects.create(
                    hospital=hospital,
                    department=department,
                    created_by=created_by,
                    title=row['title'],
                    description=row.get('description', ''),
                    start_date=parse_date(row['start_date']),
                    end_date=parse_date(row['end_date']),
                    slots=int(row['slots']),
                    available_slots=int(row['slots']),
                    specialty=row.get('specialty', ''),
                    requirements=row.get('requirements', ''),
                    status='draft',
                    validation_status='pending'
                )
                result['created_ids'].append(offer.id)
                result['success'] += 1
                
    except json.JSONDecodeError as e:
        result['errors'].append(f"Invalid JSON: {str(e)}")
    except Exception as e:
        result['errors'].append(f"Import failed: {str(e)}")
    
    return result


def export_offers_csv(queryset):
    """Export offers to CSV format."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'id', 'title', 'description', 'department', 'hospital',
        'start_date', 'end_date', 'slots', 'available_slots',
        'specialty', 'requirements', 'status', 'validation_status'
    ])
    
    for offer in queryset:
        writer.writerow([
            offer.id,
            offer.title,
            offer.description,
            offer.department.name if offer.department else '',
            offer.hospital.name,
            offer.start_date.strftime('%Y-%m-%d') if offer.start_date else '',
            offer.end_date.strftime('%Y-%m-%d') if offer.end_date else '',
            offer.slots,
            offer.available_slots,
            offer.specialty,
            offer.requirements,
            offer.status,
            offer.validation_status
        ])
    
    return output.getvalue()


def export_offers_json(queryset):
    """Export offers to JSON format."""
    offers = []
    
    for offer in queryset:
        offers.append({
            'id': offer.id,
            'title': offer.title,
            'description': offer.description,
            'department': offer.department.name if offer.department else None,
            'hospital': offer.hospital.name,
            'start_date': offer.start_date.strftime('%Y-%m-%d') if offer.start_date else None,
            'end_date': offer.end_date.strftime('%Y-%m-%d') if offer.end_date else None,
            'slots': offer.slots,
            'available_slots': offer.available_slots,
            'specialty': offer.specialty,
            'requirements': offer.requirements,
            'status': offer.status,
            'validation_status': offer.validation_status
        })
    
    return json.dumps({'offers': offers}, indent=2)


def get_import_template_csv():
    """Return CSV template for imports."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'title', 'description', 'department', 'start_date', 'end_date',
        'slots', 'specialty', 'requirements'
    ])
    writer.writerow([
        'Example Internship', 'Description here', 'Cardiology',
        '2025-01-15', '2025-03-15', '5', 'medicine_generale', 'Requirements'
    ])
    return output.getvalue()
