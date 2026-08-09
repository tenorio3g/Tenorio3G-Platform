from __future__ import annotations

from sqlalchemy import select

from app.foundation.database import SessionLocal

from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.models import DocumentModel
from app.domains.assets.documents.repositories.document_repository import (
    DocumentRepository,
)


class SQLiteDocumentRepository(
    DocumentRepository,
):
    """
    Implementación SQLite del repositorio de documentos.
    """

    def __init__(
        self,
        session_factory=SessionLocal,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        document: Document,
    ) -> None:

        clean_code = document.code.strip()

        with self._session_factory() as session:

            model = session.scalar(
                select(DocumentModel).where(
                    DocumentModel.code == clean_code
                )
            )

            if model is None:

                model = DocumentModel(
                    code=clean_code,
                    asset_code=document.asset_code.strip(),
                    title=document.title,
                    document_type=document.document_type,
                    file_name=document.file_name,
                    description=document.description,
                    revision=document.revision,
                    created_at=document.created_at,
                )

                session.add(model)

            else:

                model.asset_code = document.asset_code.strip()
                model.title = document.title
                model.document_type = document.document_type
                model.file_name = document.file_name
                model.description = document.description
                model.revision = document.revision
                model.created_at = document.created_at

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> Document | None:

        clean_code = code.strip()

        if not clean_code:
            return None

        with self._session_factory() as session:

            model = session.scalar(
                select(DocumentModel).where(
                    DocumentModel.code == clean_code
                )
            )

            if model is None:
                return None

            return self._to_entity(model)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Document]:

        clean_asset_code = asset_code.strip()

        if not clean_asset_code:
            return []

        with self._session_factory() as session:

            models = list(
                session.scalars(
                    select(DocumentModel).where(
                        DocumentModel.asset_code
                        == clean_asset_code
                    )
                ).all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        code: str,
    ) -> None:

        clean_code = code.strip()

        if not clean_code:
            return

        with self._session_factory() as session:

            model = session.scalar(
                select(DocumentModel).where(
                    DocumentModel.code == clean_code
                )
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

    @staticmethod
    def _to_entity(
        model: DocumentModel,
    ) -> Document:

        return Document(
            code=model.code,
            asset_code=model.asset_code,
            title=model.title,
            document_type=model.document_type,
            file_name=model.file_name,
            description=model.description,
            revision=model.revision,
            created_at=model.created_at,
        )