from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.db.models import Count, Q
from .models import User, Paragraph, WordIndex
from .serializers import UserSerializer, ParagraphSerializer, SearchSerializer
import re


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class ParagraphView(APIView):
    """
    API endpoint to submit multiple paragraphs of text.
    Splits text by two newlines, tokenizes words, indexes words to paragraphs.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'Text field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
        if not paragraphs:
            return Response({'error': 'No valid paragraphs found.'}, status=status.HTTP_400_BAD_REQUEST)

        created_paragraphs = []
        with transaction.atomic():
            for para_text in paragraphs:
                paragraph = Paragraph.objects.create(text=para_text)
                created_paragraphs.append(paragraph)
                words = set(re.findall(r'\S+', para_text.lower()))
                word_indices = [WordIndex(word=word, paragraph=paragraph) for word in words]
                WordIndex.objects.bulk_create(word_indices)

        serializer = ParagraphSerializer(created_paragraphs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchView(APIView):
    """
    API endpoint to search for a single word and return top 10 paragraphs containing that word.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        word = serializer.validated_data['word'].lower()

        paragraphs = Paragraph.objects.filter(
            word_indices__word=word
        ).annotate(
            word_count=Count('word_indices')
        ).order_by('-word_count')[:10]

        serializer = ParagraphSerializer(paragraphs, many=True)
        return Response(serializer.data)
