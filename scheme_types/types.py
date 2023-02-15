from dataclasses import dataclass
from typing import TypeVar, Generic, Callable
from enum import Enum

from scheme_types.tagged_types import TaggedClass, TaggedCustomString

T = TypeVar("T")


@dataclass(eq=True)
class ParsingResult(Generic[T]):
    index_from: int
    index_to: int
    found: T


Parser = Callable[[str, int], ParsingResult[T]]


@dataclass(eq=True)
class ScmVoid(TaggedClass):
    def __repr__(self):
        return "#<void>"


@dataclass
class ScmNil(TaggedClass):
    def __repr__(self):
        return "'()"

    def __eq__(self, other):
        return type(self) == type(other)


ProperList = tuple[T, "ProperList"] | ScmNil

ScmBoolean = bool


@dataclass
class ScmRational(TaggedClass):
    numerator: int
    denominator: int


ScmFloat = float

ScmNumber = ScmRational | ScmFloat


class InvalidOperationException(Exception):
    pass


class ScmChar(TaggedCustomString):
    def __init__(self, string):
        str.__init__(string)
        if len(self) != 1:
            raise ValueError(f"{string} is not a char!")

    def __repr__(self):
        return f"'{super().__str__()}'"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return super().__eq__(other)

    def __iadd__(self, *args, **kwargs):
        raise InvalidOperationException("the '+=' operator is undefined for chars")

    def __imul__(self, *args, **kwargs):
        raise InvalidOperationException("the '*=' operator is undefined for chars")


class ScmString(TaggedCustomString):
    def __init__(self, string):
        str.__init__(string)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return super().__eq__(other)

    def __repr__(self):
        return f'"{super().__str__()}"'


class ScmSymbol(TaggedCustomString):
    def __init__(self, string):
        str.__init__(string)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return super().__eq__(other)

    def __repr__(self):
        return f"'{super().__str__()}"


ScmVector = list["SExp"]
ScmPair = tuple["SExp", "SExp"]

SExp = ScmVoid | ScmNil | ScmBoolean | ScmChar | ScmString | ScmSymbol | ScmNumber | ScmVector | ScmPair


@dataclass(eq=True)
class ScmVar(TaggedClass):
    name: str


@dataclass(eq=True)
class LambdaSimple(TaggedClass):
    pass


@dataclass(eq=True)
class LambdaOpt(TaggedClass):
    opt: str


LambdaKind = LambdaSimple | LambdaOpt


@dataclass(eq=True)
class ScmConst(TaggedClass):
    sexpr: SExp


@dataclass(eq=True)
class ScmVarGet(TaggedClass):
    var: ScmVar


@dataclass(eq=True)
class ScmIf(TaggedClass):
    test: "Expr"
    dit: "Expr"
    dif: "Expr"


@dataclass(eq=True)
class ScmSeq(TaggedClass):
    exprs: list["Expr"]


@dataclass(eq=True)
class ScmOr(TaggedClass):
    exprs: list["Expr"]


@dataclass(eq=True)
class ScmVarSet(TaggedClass):
    var: ScmVar
    val: "Expr"


@dataclass(eq=True)
class ScmVarDef(TaggedClass):
    var: ScmVar
    val: "Expr"


@dataclass(eq=True)
class ScmLambda(TaggedClass):
    params: list[str]
    kind: LambdaKind
    body: "Expr"


@dataclass(eq=True)
class ScmApplic(TaggedClass):
    applicative: "Expr"
    params: list["Expr"]


Expr = ScmConst | ScmVarGet | ScmIf | ScmSeq | ScmOr | ScmVarSet | ScmVarDef | ScmLambda | ScmApplic


class AppKind(Enum):
    Tail_Call = 0
    Non_Tail_Call = 1


@dataclass(eq=True)
class Free(TaggedClass):
    pass


@dataclass(eq=True)
class Param(TaggedClass):
    minor: int


@dataclass(eq=True)
class Bound(TaggedClass):
    major: int
    minor: int


LexicalAddress = Free | Param | Bound


@dataclass(eq=True)
class ScmVarTag(TaggedClass):
    name: str
    lexical_address: LexicalAddress


ScmConstTag = ScmConst


@dataclass(eq=True)
class ScmVarGetTag(TaggedClass):
    var: ScmVarTag


@dataclass(eq=True)
class ScmIfTag(TaggedClass):
    test: "ExprTag"
    dit: "ExprTag"
    dif: "ExprTag"


@dataclass(eq=True)
class ScmSeqTag(TaggedClass):
    exprs: list["ExprTag"]


@dataclass(eq=True)
class ScmOrTag(TaggedClass):
    exprs: list["ExprTag"]


@dataclass(eq=True)
class ScmVarSetTag(TaggedClass):
    var: ScmVarTag
    val: "ExprTag"


@dataclass(eq=True)
class ScmVarDefTag(TaggedClass):
    var: ScmVarTag
    val: "ExprTag"


@dataclass(eq=True)
class ScmBoxTag(TaggedClass):
    var: ScmVarTag


@dataclass(eq=True)
class ScmBoxGetTag(TaggedClass):
    var: ScmVarTag


@dataclass(eq=True)
class ScmBoxSetTag(TaggedClass):
    var: ScmVarTag
    val: "ExprTag"


@dataclass(eq=True)
class ScmLambdaTag(TaggedClass):
    params: list[str]
    kind: LambdaKind
    body: "ExprTag"


@dataclass(eq=True)
class ScmApplicTag(TaggedClass):
    applicative: "ExprTag"
    params: list["ExprTag"]
    kind: AppKind


ExprTag = ScmConstTag | ScmVarGetTag | ScmIfTag | ScmSeqTag | ScmOrTag | ScmVarSetTag | \
          ScmVarDefTag | ScmBoxTag | ScmBoxGetTag | ScmBoxSetTag | ScmLambdaTag | ScmApplicTag
