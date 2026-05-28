from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Wallet.objects.filter(user=self.request.user)

        if self.action == "list":
            return queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        wallet = self.get_object()
        wallet.is_active = True
        wallet.save()
        serializer = self.get_serializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def deleted(self, request):
        wallets = Wallet.objects.filter(user=self.request.user, is_active=False)
        serializer = self.get_serializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
