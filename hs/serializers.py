from rest_framework import serializers


class HSPredictSerializer(serializers.Serializer):
    description = serializers.CharField()
    origin_country = serializers.CharField(required=False)
    schedule_type = serializers.ChoiceField(choices=["import", "export"])


class HSAnalyzeSerializer(serializers.Serializer):
    hs_code = serializers.CharField()
    schedule_type = serializers.ChoiceField(choices=["import", "export"])


class HSSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    schedule_type = serializers.ChoiceField(choices=["import", "export"])


class HSAskSerializer(serializers.Serializer):
    question = serializers.CharField()
