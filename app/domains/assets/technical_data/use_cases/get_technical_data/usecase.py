class GetTechnicalDataUseCase:

    def __init__(

        self,

        repository,

    ):

        self._repository = repository


    def execute(

        self,

        query,

    ):

        technical_data = (

            self._repository.get_by_asset_code(

                query.asset_code

            )

        )

        if technical_data is None:

            return GetTechnicalDataResult(

                success=False,

                message="No existe información técnica.",

            )

        return GetTechnicalDataResult(

            success=True,

            technical_data=technical_data,

        )