# auth.py app\api\endpoints
Import "app.schemas.auth" could not be resolved
"get_current_user" is unknown import symbol
# reviews.py app\api\endpoints
Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__getitem__"
  "Column[int]" is not assignable to "int"
Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__setitem__"
  "Column[int]" is not assignable to "int"
No overloads for "round" match the provided arguments
Argument of type "ColumnElement[_NUMERIC] | float" cannot be assigned to parameter "number" of type "_SupportsRound2[_T@round]" in function "round"
  Type "ColumnElement[_NUMERIC] | float" is not assignable to type "_SupportsRound2[float]"
    "ColumnElement[_NUMERIC]" is incompatible with protocol "_SupportsRound2[float]"
      "__round__" is not present
# __init__.py app\schemas
Import "app.schemas.auth" could not be resolved
# auth_service.py app\services
Argument of type "Column[str]" cannot be assigned to parameter "hashed_password" of type "str" in function "verify_password"
  "Column[str]" is not assignable to "str"

