from rest_framework import serializers

from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "category_type",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        name = attrs.get("name", getattr(self.instance, "name", None))
        category_type = attrs.get(
            "category_type",
            getattr(self.instance, "category_type", None),
        )

        category_exists = Category.objects.filter(
            user=user,
            name=name,
            category_type=category_type,
        )

        if self.instance:
            category_exists = category_exists.exclude(pk=self.instance.pk)

        if category_exists.exists():
            raise serializers.ValidationError(
                {"name": "Category with this name and type already exists."}
            )

        return attrs
