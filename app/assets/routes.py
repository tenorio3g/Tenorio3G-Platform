from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from . import assets

from app.assets.services.asset_service import (
    AssetService,
)

from app.domains.assets.bootstrap import (
    get_asset_life_sheet,
)

from app.domains.assets.use_cases.get_asset_life_sheet.query import (
    GetAssetLifeSheetQuery,
)

from app.assets.presenters.asset_life_sheet_presenter import (
    AssetLifeSheetPresenter,
)

from app.assets.presenters.asset_api_presenter import (
    AssetApiPresenter,
)


# ============================================================
# TECHNICAL DATA
# ============================================================

from app.domains.assets.technical_data.bootstrap import (
    get_technical_data,
    save_technical_data,
)

from app.domains.assets.technical_data.use_cases.get_technical_data import (
    GetTechnicalDataQuery,
)

from app.domains.assets.technical_data.use_cases.save_technical_data import (
    SaveTechnicalDataCommand,
)

from app.assets.presenters.technical_data_presenter import (
    TechnicalDataPresenter,
)


# ============================================================
# SPARE PARTS
# ============================================================

from app.domains.assets.spare_parts.bootstrap import (
    get_spare_parts_by_asset,
    save_spare_part,
)

from app.domains.assets.spare_parts.use_cases.get_spare_parts_by_asset import (
    GetSparePartsByAssetQuery,
)

from app.domains.assets.spare_parts.use_cases.save_spare_part import (
    SaveSparePartCommand,
)

from app.assets.presenters.spare_parts_presenter import (
    SparePartsPresenter,
)

from app.domains.assets.spare_parts.bootstrap import (
    delete_spare_part,
)

from app.domains.assets.spare_parts.use_cases.delete_spare_part import (
    DeleteSparePartCommand,
)


# ============================================================
# DOCUMENTS
# ============================================================
from pathlib import Path
from tempfile import NamedTemporaryFile

from werkzeug.utils import secure_filename


from app.domains.assets.documents.bootstrap import (
    create_document,
    delete_document,
    document_storage,
    get_document,
    list_documents_by_asset,
    update_document,
)
from app.domains.assets.documents.use_cases.delete_document import (
    DeleteDocumentCommand,
)

from app.domains.assets.documents.use_cases.create_document import (
    CreateDocumentCommand,
)

from app.domains.assets.documents.use_cases.list_documents_by_asset import (
    ListDocumentsByAssetQuery,
)

from app.domains.assets.documents.presentation import (
    DocumentsPresenter,
)


from app.domains.assets.documents.use_cases.get_document import (
    GetDocumentQuery,
)

from app.domains.assets.documents.use_cases.update_document import (
    UpdateDocumentCommand,
)



# ============================================================
# ASSETS INDEX
# ============================================================

@assets.route("/activos")
def index():
    """
    Pantalla principal del módulo Assets.
    """

    activos = AssetService.get_assets()

    return render_template(
        "pages/assets_index.html",
        activos=activos,
        termino_busqueda="",
    )


# ============================================================
# ASSET DETAIL
# ============================================================

@assets.route("/activo/<string:codigo>")
def asset_detail(codigo: str):
    """
    Muestra la Hoja de Vida del activo.
    """

    # --------------------------------------------------------
    # Asset principal
    # --------------------------------------------------------

    result = get_asset_life_sheet.execute(
        GetAssetLifeSheetQuery(
            code=codigo,
        )
    )

    if not result.success:
        return (
            render_template(
                "pages/asset_not_found.html",
                codigo=codigo,
            ),
            404,
        )

    activo = AssetLifeSheetPresenter.present(
        asset=result.asset,
        asset_model=result.asset_model,
    )

    # --------------------------------------------------------
    # Datos técnicos
    # --------------------------------------------------------

    technical_result = get_technical_data.execute(
        GetTechnicalDataQuery(
            asset_code=codigo,
        )
    )

    technical_data = None

    if technical_result.success:
        technical_data = TechnicalDataPresenter.present(
            technical_result.technical_data,
        )

    # --------------------------------------------------------
    # Refacciones
    # --------------------------------------------------------

    spare_parts_result = (
        get_spare_parts_by_asset.execute(
            GetSparePartsByAssetQuery(
                asset_code=codigo,
            )
        )
    )

    spare_parts = SparePartsPresenter.present(
        spare_parts_result.spare_parts
    )

# --------------------------------------------------------
# Documentos técnicos
# --------------------------------------------------------

    documents_result = list_documents_by_asset.execute(
        ListDocumentsByAssetQuery(
            asset_code=codigo,
        )
    )

    documents = DocumentsPresenter.present(
        documents_result.documents
    )





    # DEBUG TEMPORAL
    print(
        "REFACCIONES LEÍDAS:",
        len(spare_parts_result.spare_parts),
    )

    print(
        "VIEWMODEL ITEMS:",
        len(spare_parts.items),
    )

    for item in spare_parts.items:
        print(
            item.code,
            item.name,
            item.quantity,
        )

    # --------------------------------------------------------
    # Vista
    # --------------------------------------------------------

    return render_template(
        "pages/asset_detail.html",
        activo=activo,
        technical_data=technical_data,
        spare_parts=spare_parts,
        documents=documents,
    )






# ============================================================
# CREATE DOCUMENT
# ============================================================

@assets.route(
    "/activo/<string:codigo>/documentos/nuevo",
    methods=["GET", "POST"],
)
def create_document_route(codigo: str):
    """
    Registra un documento técnico asociado a un activo.
    """

    if request.method == "POST":

        uploaded_file = request.files.get(
            "document_file"
        )

        stored_file_name = request.form.get(
            "file_name",
            "",
        )

        if (
            uploaded_file
            and uploaded_file.filename
        ):
            original_name = secure_filename(
                uploaded_file.filename
            )

            extension = Path(
                original_name
            ).suffix.lower()

            if extension != ".pdf":
                return (
                    "Solo se permiten archivos PDF.",
                    400,
                )

            safe_code = secure_filename(
                request.form.get(
                    "code",
                    "",
                )
            )

            stored_file_name = (
                f"{safe_code}__{original_name}"
            )

            with NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temporary_file:

                temporary_path = Path(
                    temporary_file.name
                )

                uploaded_file.save(
                    temporary_file
                )

            try:
                document_storage.save(
                    temporary_path,
                    stored_file_name,
                )
            finally:
                temporary_path.unlink(
                    missing_ok=True
                )

        result = create_document.execute(
            CreateDocumentCommand(
                code=request.form.get(
                    "code",
                    "",
                ),
                asset_code=codigo,
                title=request.form.get(
                    "title",
                    "",
                ),
                document_type=request.form.get(
                    "document_type",
                    "",
                ),
                file_name=stored_file_name,
                description=request.form.get(
                    "description",
                    "",
                ),
                revision=request.form.get(
                    "revision",
                    "",
                ),
            )
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    return render_template(
        "pages/create_document.html",
        codigo=codigo,
    )









# ============================================================
# ASSET API
# ============================================================

@assets.get("/assets/api/<string:codigo>")
def asset_api(codigo: str):
    """
    Devuelve la Hoja de Vida del activo en formato JSON.
    """

    result = get_asset_life_sheet.execute(
        GetAssetLifeSheetQuery(
            code=codigo,
        )
    )

    if not result.success:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.message,
                    "codigo": codigo,
                }
            ),
            404,
        )

    view_model = AssetLifeSheetPresenter.present(
        asset=result.asset,
        asset_model=result.asset_model,
    )

    payload = AssetApiPresenter.present(
        view_model,
    )

    return jsonify(payload)


# ============================================================
# EDIT TECHNICAL DATA
# ============================================================

@assets.route(
    "/activo/<string:codigo>/editar-datos-tecnicos",
    methods=["GET", "POST"],
)
def edit_technical_data(codigo: str):
    """
    Consulta y actualiza los datos técnicos del activo.
    """

    if request.method == "POST":

        result = save_technical_data.execute(
            SaveTechnicalDataCommand(
                asset_code=codigo,
                equipment_type=request.form.get(
                    "equipment_type",
                    "",
                ),
                manufacturer=request.form.get(
                    "manufacturer",
                    "",
                ),
                model=request.form.get(
                    "model",
                    "",
                ),
                serial_number=request.form.get(
                    "serial_number",
                    "",
                ),
                voltage=request.form.get(
                    "voltage",
                    "",
                ),
                phases=request.form.get(
                    "phases",
                    "",
                ),
                frequency=request.form.get(
                    "frequency",
                    "",
                ),
                motor_power=request.form.get(
                    "motor_power",
                    "",
                ),
                observations=request.form.get(
                    "observations",
                    "",
                ),
            )
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    technical_result = get_technical_data.execute(
        GetTechnicalDataQuery(
            asset_code=codigo,
        )
    )

    technical_data = None

    if technical_result.success:
        technical_data = TechnicalDataPresenter.present(
            technical_result.technical_data,
        )

    return render_template(
        "pages/edit_technical_data.html",
        codigo=codigo,
        technical_data=technical_data,
    )


# ============================================================
# CREATE SPARE PART
# ============================================================

@assets.route(
    "/activo/<string:codigo>/refacciones/nueva",
    methods=["GET", "POST"],
)
def create_spare_part(codigo: str):
    """
    Registra una nueva refacción asociada a un activo.
    """

    if request.method == "POST":

        print("POST recibido")
        print(request.form.to_dict())

        try:
            quantity = float(
                request.form.get(
                    "quantity",
                    "1",
                )
            )

        except ValueError:
            quantity = 0

        result = save_spare_part.execute(
            SaveSparePartCommand(
                asset_code=codigo,
                code=request.form.get(
                    "code",
                    "",
                ),
                name=request.form.get(
                    "name",
                    "",
                ),
                manufacturer=request.form.get(
                    "manufacturer",
                    "",
                ),
                part_number=request.form.get(
                    "part_number",
                    "",
                ),
                unit=request.form.get(
                    "unit",
                    "pieza",
                ),
                quantity=quantity,
                position=request.form.get(
                    "position",
                    "",
                ),
                observations=request.form.get(
                    "observations",
                    "",
                ),
                is_critical=(
                    request.form.get(
                        "is_critical"
                    )
                    == "on"
                ),
            )
        )

        print(
            "Resultado:",
            result.success,
            result.message,
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    return render_template(
        "pages/create_spare_part.html",
        codigo=codigo,
    )



@assets.route(
    "/activo/<string:codigo>/refacciones/<string:spare_part_code>/editar",
    methods=["GET", "POST"],
)
def edit_spare_part(
    codigo: str,
    spare_part_code: str,
):
    """
    Edita una refacción asociada a un activo.
    """

    spare_parts_result = get_spare_parts_by_asset.execute(
        GetSparePartsByAssetQuery(
            asset_code=codigo,
        )
    )

    relation = next(
        (
            item
            for item in spare_parts_result.spare_parts
            if item.spare_part_code == spare_part_code
        ),
        None,
    )

    if relation is None:
        return (
            render_template(
                "pages/spare_part_not_found.html",
                codigo=codigo,
                spare_part_code=spare_part_code,
            ),
            404,
        )

    if request.method == "POST":

        try:
            quantity = float(
                request.form.get(
                    "quantity",
                    "1",
                )
            )
        except ValueError:
            quantity = 0

        result = save_spare_part.execute(
            SaveSparePartCommand(
                asset_code=codigo,

                # El código permanece fijo durante edición.
                code=spare_part_code,

                name=request.form.get(
                    "name",
                    "",
                ),
                manufacturer=request.form.get(
                    "manufacturer",
                    "",
                ),
                part_number=request.form.get(
                    "part_number",
                    "",
                ),
                unit=request.form.get(
                    "unit",
                    "pieza",
                ),
                quantity=quantity,
                position=request.form.get(
                    "position",
                    "",
                ),
                observations=request.form.get(
                    "observations",
                    "",
                ),
                is_critical=(
                    request.form.get("is_critical")
                    == "on"
                ),
            )
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    return render_template(
        "pages/edit_spare_part.html",
        codigo=codigo,
        relation=relation,
    )

@assets.post(
    "/activo/<string:codigo>/refacciones/"
    "<string:spare_part_code>/eliminar"
)
def delete_spare_part_route(
    codigo: str,
    spare_part_code: str,
):

    result = delete_spare_part.execute(
        DeleteSparePartCommand(
            asset_code=codigo,
            spare_part_code=spare_part_code,
        )
    )

    return redirect(
        url_for(
            "assets.asset_detail",
            codigo=codigo,
        )
    )



# ============================================================
# EDIT DOCUMENT
# ============================================================

@assets.route(
    "/activo/<string:codigo>/documentos/<string:document_code>/editar",
    methods=["GET", "POST"],
)
def edit_document_route(
    codigo: str,
    document_code: str,
):
    """
    Edita los metadatos de un documento técnico.
    """

    document_result = get_document.execute(
        GetDocumentQuery(
            code=document_code,
        )
    )

    document = document_result.document

    if document is None or document.asset_code != codigo:
        return (
            render_template(
                "pages/document_not_found.html",
                codigo=codigo,
                document_code=document_code,
            ),
            404,
        )

    if request.method == "POST":

        result = update_document.execute(
            UpdateDocumentCommand(
                code=document_code,
                asset_code=codigo,
                title=request.form.get(
                    "title",
                    "",
                ),
                document_type=request.form.get(
                    "document_type",
                    "",
                ),
                file_name=request.form.get(
                    "file_name",
                    "",
                ),
                description=request.form.get(
                    "description",
                    "",
                ),
                revision=request.form.get(
                    "revision",
                    "",
                ),
            )
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    return render_template(
        "pages/edit_document.html",
        codigo=codigo,
        document=document,
    )




# ============================================================
# DELETE DOCUMENT
# ============================================================

@assets.post(
    "/activo/<string:codigo>/documentos/"
    "<string:document_code>/eliminar"
)
def delete_document_route(
    codigo: str,
    document_code: str,
):
    """
    Elimina un documento técnico asociado a un activo.
    """

    document_result = get_document.execute(
        GetDocumentQuery(
            code=document_code,
        )
    )

    document = document_result.document

    if document is None or document.asset_code != codigo:
        return (
            render_template(
                "pages/document_not_found.html",
                codigo=codigo,
                document_code=document_code,
            ),
            404,
        )

    file_name = document.file_name

    result = delete_document.execute(
        DeleteDocumentCommand(
            code=document_code,
        )
    )

    if result.success:

        if (
            file_name
            and document_storage.exists(
                file_name
            )
        ):
            document_storage.delete(
                file_name
            )

        return redirect(
            url_for(
                "assets.asset_detail",
                codigo=codigo,
            )
        )

    return  (
        "No se pudo eliminar el documento.",
        400,
    )



# ============================================================
# VIEW DOCUMENT
# ============================================================

@assets.get(
    "/activo/<string:codigo>/documentos/"
    "<string:document_code>/ver"
)
def view_document_route(
    codigo: str,
    document_code: str,
):
    """
    Entrega un documento técnico asociado a un activo.
    """

    document_result = get_document.execute(
        GetDocumentQuery(
            code=document_code,
        )
    )

    document = document_result.document

    if document is None or document.asset_code != codigo:
        return (
            render_template(
                "pages/document_not_found.html",
                codigo=codigo,
                document_code=document_code,
            ),
            404,
        )

    if not document_storage.exists(
        document.file_name
    ):
        return (
            "Archivo físico no encontrado.",
            404,
        )

    file_path = document_storage.get_path(
        document.file_name
    )

    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=document.file_name,
    )