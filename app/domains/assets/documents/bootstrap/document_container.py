from app.domains.assets.documents.repositories import (
    SQLiteDocumentRepository,
)

from app.domains.assets.documents.use_cases.create_document import (
    CreateDocument,
)

from app.domains.assets.documents.use_cases.get_document import (
    GetDocument,
)

from app.domains.assets.documents.use_cases.list_documents_by_asset import (
    ListDocumentsByAsset,
)

from app.domains.assets.documents.use_cases.update_document import (
    UpdateDocument,
)

from app.domains.assets.documents.use_cases.delete_document import (
    DeleteDocument,
)


document_repository = SQLiteDocumentRepository()


create_document = CreateDocument(
    document_repository,
)

get_document = GetDocument(
    document_repository,
)

list_documents_by_asset = ListDocumentsByAsset(
    document_repository,
)

update_document = UpdateDocument(
    document_repository,
)

delete_document = DeleteDocument(
    document_repository,
)