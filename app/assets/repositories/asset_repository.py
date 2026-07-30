from app.assets.domain.asset import Asset
from app.shared.constants import AssetStatus


class AssetRepository:
    """
    Repositorio temporal de activos.

    Actualmente utiliza información de prueba almacenada en código.
    En el futuro podrá conectarse a una base de datos sin modificar
    la forma en que las rutas consultan los activos.
    """

    CODIGO_ES09 = "ES09"

    @staticmethod
    def _crear_catalogo() -> list[Asset]:
        """
        Crea y devuelve el catálogo temporal de activos.

        Cada consulta genera nuevas instancias para evitar que los eventos
        o cambios temporales de un activo afecten consultas posteriores.

        Returns:
            Lista de activos disponibles en el repositorio temporal.
        """

        activo_es09 = Asset(
            codigo="S2-480-ES09-T269",
            nombre="TABLERO GENERAL ES09",
            estado=AssetStatus.OPERANDO,
            ubicacion="Subestación Norte",
            area="Producción",
            salud=84,
            ultimo_mantenimiento="18 Junio 2026",
            proximo_mantenimiento="18 Septiembre 2026",
        )

        activo_es09.agregar_evento(
            title="Inspección visual",
            description=(
                "Se realizó una inspección general del tablero "
                "sin detectar anomalías visibles."
            ),
            event_type="Inspección",
            created_by="Ing. Fortunato Tenorio",
        )

        activo_es09.agregar_evento(
            title="Inspección termográfica",
            description=(
                "Se verificaron las conexiones principales y no "
                "se detectaron puntos calientes críticos."
            ),
            event_type="Termografía",
            created_by="Daniel Hernández",
        )

        return [activo_es09]

    @staticmethod
    def obtener_todos() -> list[Asset]:
        """
        Devuelve todos los activos registrados.

        Returns:
            Lista completa de activos disponibles.
        """

        return AssetRepository._crear_catalogo()

    @staticmethod
    def obtener_por_codigo(codigo: str) -> Asset | None:
        """
        Busca un activo mediante su código corto o código completo.

        Ejemplos válidos:
            ES09
            S2-480-ES09-T269

        Args:
            codigo: Código utilizado para localizar el activo.

        Returns:
            El activo encontrado o None cuando no existe o el código
            proporcionado no es válido.
        """

        termino = AssetRepository._normalizar_texto(codigo)

        if not termino:
            return None

        for activo in AssetRepository._crear_catalogo():
            codigo_completo = AssetRepository._normalizar_texto(
                activo.codigo
            )

            if termino == codigo_completo:
                return activo

            if termino == AssetRepository.CODIGO_ES09:
                return activo

        return None

    @staticmethod
    def buscar(consulta: str) -> list[Asset]:
        """
        Busca activos por código, nombre, ubicación o área.

        La búsqueda no distingue entre mayúsculas, minúsculas ni
        espacios al principio o al final.

        Args:
            consulta: Texto escrito por el usuario.

        Returns:
            Lista de activos que coinciden con la consulta.
            Si la consulta está vacía, devuelve todos los activos.
        """

        termino = AssetRepository._normalizar_texto(consulta)
        activos = AssetRepository._crear_catalogo()

        if not termino:
            return activos

        resultados = []

        for activo in activos:
            campos_busqueda = (
                activo.codigo,
                activo.nombre,
                activo.ubicacion,
                activo.area,
            )

            coincide = any(
                termino in AssetRepository._normalizar_texto(campo)
                for campo in campos_busqueda
            )

            codigo_corto_coincide = (
                termino in AssetRepository.CODIGO_ES09
            )

            if coincide or codigo_corto_coincide:
                resultados.append(activo)

        return resultados

    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        """
        Normaliza un valor para utilizarlo en comparaciones y búsquedas.

        Args:
            valor: Valor que se desea normalizar.

        Returns:
            Texto sin espacios externos y convertido a mayúsculas.
            Devuelve una cadena vacía cuando el valor no es texto.
        """

        if not isinstance(valor, str):
            return ""

        return valor.strip().upper()