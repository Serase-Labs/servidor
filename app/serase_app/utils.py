from rest_framework import serializers

def required_params(dic, required_list):
    for required in required_list:
        if required not in dic:
            raise serializers.ValidationError({required: "Campo obrigatório não está presente."})
    return True