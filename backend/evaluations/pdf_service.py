"""
PDF generation service for evaluation reports.
Uses weasyprint if available, falls back to HTML download.
"""
from django.template.loader import render_to_string
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint not installed. PDF generation will return HTML.")


def generate_evaluation_pdf(evaluation):
    """
    Generate PDF for an evaluation report.
    
    Args:
        evaluation: Evaluation model instance
        
    Returns:
        HttpResponse with PDF content or HTML fallback
    """
    context = {
        'evaluation': evaluation,
    }
    html_content = render_to_string('pdf/evaluation_report.html', context)
    
    if WEASYPRINT_AVAILABLE:
        try:
            html = HTML(string=html_content)
            pdf_content = html.write_pdf()
            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            filename = f"evaluation_{evaluation.internship.student.student_number}_{evaluation.id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
    
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'inline; filename="evaluation_{evaluation.id}.html"'
    return response


def generate_evaluation_pdf_bytes(evaluation):
    """
    Generate PDF bytes for an evaluation (for email attachments).
    
    Returns:
        bytes: PDF content or None if generation fails
    """
    if not WEASYPRINT_AVAILABLE:
        return None
        
    try:
        context = {'evaluation': evaluation}
        html_content = render_to_string('pdf/evaluation_report.html', context)
        html = HTML(string=html_content)
        return html.write_pdf()
    except Exception as e:
        logger.error(f"PDF bytes generation failed: {str(e)}")
        return None
