from typing import Callable, Collection, Mapping, ClassVar, Any
from collections.abc import Sequence
import warnings
from airflow.sdk import Context
from airflow.sdk.bases.decorators import DecoratedOperator
from airflow.sdk.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.providers.definitions._internal.types import SET_DURING_EXECUTION
from airflow.utils.context import context_merge
from airflow.utils.operator_helpers import determine_kwargs
from airflow.sdk.bases.decorator import TaskDecorator, task_decorator_factory


class _SQLDecoratedOperator(DecoratedOperator, SQLExecuteQueryOperator):

    template_fields: Sequence[str] = (*DecoratedOperator.template_fields, *SQLExecuteQueryOperator.template_fields)
    template_fields_renderers: ClassVar[dict[str, str]] = {
        **DecoratedOperator.template_fields_renderers,
        **SQLExecuteQueryOperator.template_fields_renderers,
    }

    custom_operator_name: str = "@task.sql"
    # internal attribute related to templated fields
    overwrite_rtif_after_execution: bool = False

    def __init__(
            self,
            *,
            python_callable: Callable,
            op_args: Collection[Any] | None = None,
            op_kwargs: Mapping[str, Any] | None = None,
            **kwargs
    ) -> None:
        
        if kwargs.pop("multiple_outputs", None):
            warnings.warn(
                f"`multiple_outputs=True` is not supported in {self.custom_operator_name} tasks. Ignoring.",
                UserWarning,
                stacklevel = 3
            )

        super().__init__(
            python_callable = python_callable,
            op_args = op_args,
            op_kwargs = op_kwargs,
            sql = SET_DURING_EXECUTION,
            multiple_outputs = False,
            **kwargs
        )

    def execute(self, context: Context) -> None:
        context_merge(context, self.op_kwargs)
        
        kwargs = determine_kwargs(self.python_callable, self.op_args, context)

        # this return python function that will return sql query
        self.sql = self.python_callable(*self.op_args, **kwargs)

        if not isinstance(self.sql, str) or not self.sql.strip():
            raise TypeError("The returned value from TaskFlow callable must be non-empty string")
        
        # redner templates of string
        context['ti'].render_templates()

        # execute context from SQLExecuteQueryOperator
        return super().execute(context)
    

def sql_task(
    python_callable: Callable | None = None,
    **kwargs
) -> TaskDecorator:
    return task_decorator_factory(
        python_callable = python_callable,
        decorated_operator_class = _SQLDecoratedOperator,
        **kwargs
    )