from rest_framework import serializers

class AskRequestSerializer(serializers.Serializer):
    query = serializers.CharField()
    top_k = serializers.IntegerField(default=5)


class SourceSerializer(serializers.Serializer):
    content = serializers.CharField()
    doc_level = serializers.CharField()


class AskResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    sources = SourceSerializer(many=True)