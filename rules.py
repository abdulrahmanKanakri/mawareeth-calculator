from experta import P, NOT, OR, AND
from facts import *


def has_sons():
    return Sons(P(lambda x: x > 0))


def has_no_sons():
    return NOT(has_sons())


def has_daughters():
    return Daughters(P(lambda x: x > 0))


def has_no_daughters():
    return NOT(has_daughters())


def has_sons_of_sons():
    return SonsOfSons(P(lambda x: x > 0))


def has_no_sons_of_sons():
    return NOT(has_sons_of_sons())


def has_daughters_of_sons():
    return DaughtersOfSons(P(lambda x: x > 0))


def has_no_daughters_of_sons():
    return NOT(has_daughters_of_sons())


def has_father():
    return Father("alive")


def has_no_father():
    return NOT(has_father())


def has_mother():
    return Mother("alive")


def has_no_mother():
    return NOT(has_mother())


def has_fathers_father():
    return FathersFather("alive")


def has_no_fathers_father():
    return NOT(has_fathers_father())


def has_full_brother():
    return FullBrother(P(lambda x: x > 0))


def has_no_full_brother():
    return NOT(has_full_brother())


def has_full_sister():
    return FullSister(P(lambda x: x > 0))


def has_no_full_sister():
    return NOT(has_full_sister())


def has_brothers_from_father():
    return BrotherFromFather(P(lambda x: x > 0))


def has_no_brothers_from_father():
    return NOT(has_brothers_from_father())


def has_sisters_from_father():
    return SisterFromFather(P(lambda x: x > 0))


def has_no_sisters_from_father():
    return NOT(has_sisters_from_father())


def has_daughters_or_daughters_of_sons():
    return OR(Daughters(P(lambda x: x > 0)), DaughtersOfSons(P(lambda x: x > 0)))


def daughters_of_sons_rules():
    return AND(
        Sons(P(lambda x: x == 0)),
        NOT(
            AND(
                SonsOfSons(P(lambda x: x == 0)),
                Daughters(P(lambda x: x >= 2))
            )
        )
    )


def father_and_mother_are_dead():
    return AND(Father("dead"), Mother("dead"))


def has_no_father_no_sons_and_no_sons_of_sons():
    return AND(
        has_no_father(),
        has_no_sons(),
        has_no_sons_of_sons()
    )


def full_brothers_and_sisters_rules():
    return AND(
        has_no_father_no_sons_and_no_sons_of_sons(),
        NOT(FullBrother()),
        NOT(FullSister())
    )


def full_sister_became_with_others():
    return AND(
        has_full_sister(),
        has_daughters_or_daughters_of_sons()
    )


def brothers_from_father_rules():
    return AND(
        has_no_father_no_sons_and_no_sons_of_sons(),
        has_no_full_brother(),
        NOT(full_sister_became_with_others())
    )


def sisters_from_father_rules():
    return AND(
        has_no_father_no_sons_and_no_sons_of_sons(),
        has_no_full_brother(),
        NOT(
            OR(
                full_sister_became_with_others(),
                AND(
                    FullSister(P(lambda x: x >= 2)),
                    BrotherFromFather(P(lambda x: x == 0))
                )
            )
        )
    )


def brothers_and_sisters_from_mother_rules():
    return AND(
        has_no_father_no_sons_and_no_sons_of_sons(),
        has_no_daughters(),
        has_no_daughters_of_sons(),
        has_no_fathers_father(),
    )


def sister_from_father_became_with_others():
    return AND(
        has_sisters_from_father(),
        has_daughters_or_daughters_of_sons()
    )


def son_of_full_brother_rules():
    return AND(
        brothers_from_father_rules(),
        has_no_fathers_father(),
        has_no_brothers_from_father(),
        NOT(sister_from_father_became_with_others())
    )


def son_of_brother_from_father_rules():
    return AND(
        son_of_full_brother_rules(), 
        SonOfFullBrother(P(lambda x: x == 0))
    )


def full_uncle_rules():
    return AND(
        son_of_brother_from_father_rules(), 
        SonOfBrotherFromFather(P(lambda x: x == 0))
    )


def uncle_from_father_rules():
    return AND(
        full_uncle_rules(), 
        FullUncle(P(lambda x: x == 0))
    )


def son_of_full_uncle_rules():
    return AND(
        uncle_from_father_rules(), 
        UncleFromFather(P(lambda x: x == 0))
    )


def son_of_uncle_from_father():
    return AND(
        son_of_full_uncle_rules(), 
        SonOfFullUncle(P(lambda x: x == 0))
    )


def has_no_heir_branch():
    return AND(
        has_no_sons(),
        has_no_daughters(),
        has_no_sons_of_sons(),
        has_no_daughters_of_sons()
    )


def has_heir_branch():
    return NOT(has_no_heir_branch())


def full_sisters_share_rules():
    return AND(
        has_no_daughters(),
        has_no_daughters_of_sons()
    )


def sisters_from_father_share_rules():
    return AND(
        has_no_daughters(),
        has_no_daughters_of_sons(),
        has_no_full_sister()
    )


def has_collection_of_brothers_and_sisters():
    return OR(
        FullBrother(P(lambda x: x >= 2)),
        BrotherFromFather(P(lambda x: x >= 2)),
        BrotherFromMother(P(lambda x: x >= 2)),
        FullSister(P(lambda x: x >= 2)),
        SisterFromFather(P(lambda x: x >= 2)),
        SisterFromMother(P(lambda x: x >= 2)),
        AND(
            OR(
                FullBrother(P(lambda x: x == 1)),
                BrotherFromFather(P(lambda x: x == 1)),
                BrotherFromMother(P(lambda x: x == 1))
            ),
            OR(
                FullSister(P(lambda x: x == 1)),
                SisterFromFather(P(lambda x: x == 1)),
                SisterFromMother(P(lambda x: x == 1))
            )
        )
    )


def has_no_collection_of_brothers_and_sisters():
    return NOT(has_collection_of_brothers_and_sisters())


def has_collection_of_brothers_and_sisters_from_mother():
    return OR(
        BrotherFromMother(P(lambda x: x >= 2)),
        SisterFromMother(P(lambda x: x >= 2)),
        AND(
            BrotherFromMother(P(lambda x: x == 1)),
            SisterFromMother(P(lambda x: x == 1))
        )
    )


def has_heir_branch_only_girls():
    return AND(
        OR(Daughters(P(lambda x: x > 0)), DaughtersOfSons(P(lambda x: x > 0))),
        AND(Sons(P(lambda x: x == 0)), SonsOfSons(P(lambda x: x == 0))),
    )


def has_heir_branch_only_boys():
    return OR(Sons(P(lambda x: x > 0)), SonsOfSons(P(lambda x: x > 0)))


# to give mother 1/3 of rem
def omaryatan():
    return AND(
        Mother("alive"),
        Father("alive"), 
        OR(
            Husband("alive"), 
            Wives(P(lambda x: x > 0))
        ),
        has_no_heir_branch()
    )


def has_no_brother():
    return AND(has_no_brothers_from_father, has_no_full_brother)
