from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Evaluation
from .serializers import EvaluationCreateSerializer, EvaluationDetailSerializer
from auth_service.permissions import IsEncadrant
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

class CreateEvaluationView(generics.CreateAPIView):
    serializer_class = EvaluationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEncadrant]

    def perform_create(self, serializer):
        serializer.save(medecin=self.request.user)

class EvaluationDetailView(generics.RetrieveAPIView):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationPdfView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        evaluation = get_object_or_404(Evaluation, pk=pk)
        # permission check: only medecin, student (owner of stage), faculty admin allowed
        user = request.user
        allowed = False
        if getattr(user, "role", None) in ("faculty_admin", "hospital_admin"):
            allowed = True
        if evaluation.medecin_id == user.id:
            allowed = True
        if evaluation.stage.candidacy.student_id == user.id:
            allowed = True
        if not allowed:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        # generate simple PDF using ReportLab
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        text_lines = [
            f"Evaluation ID: {evaluation.id}",
            f"Stage ID: {evaluation.stage_id}",
            f"Medecin: {evaluation.medecin}",
            f"Date: {evaluation.date_evaluation.strftime('%Y-%m-%d %H:%M')}",
            "",
            "Notes:",
            f" - Competences: {evaluation.note_competences}",
            f" - Assiduite: {evaluation.note_assiduite}",
            f" - Comportement: {evaluation.note_comportement}",
            "",
            "Commentaire:",
            evaluation.commentaire or "",
        ]
        y = 800
        for line in text_lines:
            p.drawString(50, y, str(line))
            y -= 20
            if y < 50:
                p.showPage()
                y = 800
        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="evaluation_{evaluation.id}.pdf"'
        return response