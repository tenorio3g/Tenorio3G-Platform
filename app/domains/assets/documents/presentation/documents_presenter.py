from app.domains.assets.documents.entities import (
    Document,
)

from .documents_view_model import (
    DocumentItemViewModel,
    DocumentsViewModel,
)


class DocumentsPresenter:
    """
    Adapta documentos técnicos
    para mostrarlos en el expediente del activo.
    """

    @staticmethod
    def present(
        documents: list[Document],
    ) -> DocumentsViewModel:

        items = [
            DocumentItemViewModel(
                code=document.code,
                title=document.title,
                document_type=document.document_type,
                file_name=document.file_name,
                description=(
                    document.description
                    or ""
                ),
                revision=(
                    document.revision
                    or "Sin revisión"
                ),
                created_at=(
                    document.created_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    if document.created_at
                    else "Sin fecha"
                ),
            )
            for document in documents
        ]

        return DocumentsViewModel(
            items=items,
        )