from Calculator import SharesCalculator
from typing import List
from experta import *
from rules import *
from constants import *
from Share import Share


class MawarethEngine(KnowledgeEngine):

    shares: List[Share] = []
    amount = 0

    @Rule(NOT(Amount()), salience=100)
    def enter_amount(self):
        self.amount = int(input("Enter the amount of the estate: "))
        self.declare(Amount(self.amount))

    # The amount must be valid positive number
    @Rule(Amount(P(lambda x: x > 0)), NOT(Gender()), salience=99)
    def enter_gender(self):
        self.declare(Gender(input("Is the deceased male or female? ")))

    # The gender must be male or female
    @Rule(Gender(L("male") | L("female")), NOT(MaritalStatus()), salience=98)
    def enter_marital_status(self):
        self.declare(MaritalStatus(
            input("Is the deceased married, divorced, or single? ")
        ))

    # If the deceased is male and married then ask how many wives he has
    @Rule(
        Gender("male"), 
        MaritalStatus("married"), 
        NOT(Wives()), 
        salience=97
    )
    def enter_wives(self):
        self.declare(Wives(int(input("How many wives (0, 1, 2, 3, 4)? "))))

    # If the deceased is female and married then ask about the husband
    @Rule(
        Gender("female"), 
        MaritalStatus("married"), 
        NOT(Husband()), 
        salience=96
    )
    def enter_husband(self):
        self.declare(Husband(input("Is the husband alive or dead? ")))

    # If the deceased is married or divorced then ask about the children
    @Rule(
        MaritalStatus(L("married") | L("divorced")), 
        NOT(Sons()), 
        NOT(Daughters()), 
        salience=95
    )
    def enter_children(self):
        self.declare(Sons(int(input("How many sons? "))))
        self.declare(Daughters(int(input("How many daughters? "))))

    # Ask about the father and mother
    @Rule(NOT(Father()), NOT(Mother()), salience=92)
    def enter_father_and_mother(self):
        self.declare(Father(input("Is the father alive or dead? ")))
        self.declare(Mother(input("Is the mother alive or dead? ")))

    # If the deceased has no sons then ask about sons of sons
    @Rule(Sons(P(lambda x: x == 0)), NOT(SonsOfSons()), salience=94)
    def enter_sons_of_sons(self):
        self.declare(SonsOfSons(int(input("How many sons of sons? "))))

    # If the deceased has no sons and less than 2 daughters
    # then ask about daughters of sons
    @Rule(daughters_of_sons_rules(), NOT(DaughtersOfSons()), salience=93)
    def enter_daughters_of_sons(self):
        self.declare(DaughtersOfSons(
            int(input("How many daughters of sons? "))
        ))

    # If the father is dead then ask about his father
    @Rule(Father("dead"), NOT(FathersFather()), salience=17)
    def enter_grand_father(self):
        self.declare(FathersFather(
            input("Is the father's father alive or dead? ")))

    # If the mother is dead then ask about her mother
    @Rule(Mother("dead"), NOT(MothersMother()), salience=16)
    def enter_mothers_mother(self):
        self.declare(MothersMother(
            input("Is the mother's mother alive or dead? ")))

    # If the mother and father are dead then ask about father's mother
    @Rule(father_and_mother_are_dead(), NOT(FathersMother()), salience=15)
    def enter_fathers_mother(self):
        self.declare(FathersMother(
            input("Is the father's mother alive or dead? ")))

    # If the father and the sons and their sons all are dead or not exists,
    # then ask about the full brothers
    @Rule(full_brothers_and_sisters_rules(), salience=14)
    def enter_full_brothers_and_sisters(self):
        self.declare(FullBrother(int(input("How many full brothers? "))))
        self.declare(FullSister(int(input("How many full sisters? "))))

    @Rule(brothers_from_father_rules(), NOT(BrotherFromFather()), salience=13)
    def enter_brothers_from_father(self):
        self.declare(BrotherFromFather(
            int(input("How many brothers from father? "))))

    @Rule(sisters_from_father_rules(), NOT(SisterFromFather()), salience=12)
    def enter_sisters_from_father(self):
        self.declare(SisterFromFather(
            int(input("How many sisters from father? "))))

    @Rule(
        brothers_and_sisters_from_mother_rules(),
        NOT(BrotherFromMother()),
        NOT(SisterFromMother()),
        salience=11
    )
    def enter_brothers_and_sisters_from_mother(self):
        self.declare(BrotherFromMother(
            int(input("How many brothers from mother? "))))
        self.declare(SisterFromMother(
            int(input("How many sisters from mother? "))))

    @Rule(son_of_full_brother_rules(), NOT(SonOfFullBrother()), salience=10)
    def enter_son_of_full_brother(self):
        self.declare(SonOfFullBrother(
            int(input("How many sons of full brothers? "))))

    @Rule(son_of_brother_from_father_rules(), NOT(SonOfBrotherFromFather()), salience=9)
    def enter_son_of_brother_from_father(self):
        self.declare(SonOfBrotherFromFather(
            int(input("How many sons of brothers from fathers? "))))

    @Rule(full_uncle_rules(), NOT(FullUncle()), salience=8)
    def enter_full_uncle(self):
        self.declare(FullUncle(int(input("How many full uncle? "))))

    @Rule(uncle_from_father_rules(), NOT(UncleFromFather()), salience=7)
    def enter_uncle_from_father(self):
        self.declare(UncleFromFather(
            int(input("How many uncle from father? "))))

    @Rule(son_of_full_uncle_rules(), NOT(SonOfFullUncle()), salience=6)
    def enter_son_of_full_uncle(self):
        self.declare(SonOfFullUncle(
            int(input("How many sons of full uncle? "))))

    @Rule(son_of_uncle_from_father(), NOT(SonOfUncleFromFather()), salience=5)
    def enter_son_of_uncle_from_father(self):
        self.declare(SonOfUncleFromFather(
            int(input("How many sons of uncle from father? "))))

    """ Start Sharing Rules """

    # Husband Share
    @Rule(Husband("alive"), has_no_heir_branch(), NOT(HusbandShare()))
    def husband_share_1(self):
        self.declare(HusbandShare(HALF))
        self.shares.append(Share('husband', HALF))

    @Rule(Husband("alive"), has_heir_branch(), NOT(HusbandShare()))
    def husband_share_2(self):
        self.declare(HusbandShare(QUARTER))
        self.shares.append(Share('husband', QUARTER))

    # Wives Share
    @Rule(
        Wives(P(lambda x: x > 0)), 
        Wives(MATCH.count), 
        has_no_heir_branch(),
        NOT(WivesShare())
    )
    def wives_share_1(self, count):
        self.declare(WivesShare(QUARTER))
        self.shares.append(Share('wives', QUARTER, count))

    @Rule(
        Wives(P(lambda x: x > 0)), 
        Wives(MATCH.count), 
        has_heir_branch(),
        NOT(WivesShare())
    )
    def wives_share_2(self, count):
        self.declare(WivesShare(ONE_EIGHTH))
        self.shares.append(Share('wives', ONE_EIGHTH, count))

    # Father Share
    @Rule(Father("alive"), has_heir_branch_only_boys(), NOT(FatherShare()))
    def father_share(self):
        self.declare(FatherShare(ONE_SIXTH))
        self.shares.append(Share('father', ONE_SIXTH))
    
    @Rule(Father("alive"), has_heir_branch_only_girls(), NOT(FatherShare()))
    def father_takes_the_rest_and_one_over_sixth(self):
        self.declare(FatherShare(REMAINDER_AND_ONE_SIXTH))
        self.shares.append(Share('father', REMAINDER_AND_ONE_SIXTH))

    @Rule(Father("alive"), has_no_heir_branch(), NOT(FatherShare()))
    def father_takes_the_rest(self):
        self.declare(FatherShare(REMAINDER))
        self.shares.append(Share('father', REMAINDER))

    # Mother Share
    @Rule(
        Mother("alive"),
        has_no_heir_branch(),
        has_no_collection_of_brothers_and_sisters(),
        NOT(MotherShare())
    )
    def mother_share_1(self):
        self.declare(MotherShare(ONE_THIRD))
        self.shares.append(Share('mother', ONE_THIRD))

    @Rule(
        Mother("alive"),
        OR(
            has_heir_branch(),
            has_collection_of_brothers_and_sisters()
        ),
        NOT(MotherShare())
    )
    def mother_share_2(self):
        self.declare(MotherShare(ONE_SIXTH))
        self.shares.append(Share('mother', ONE_SIXTH))

    @Rule(omaryatan(), NOT(MotherShare()))
    def mother_share_3(self):
        self.declare(MotherShare(ONE_THIRD_OF_REMAINDER))
        self.shares.append(Share('mother', ONE_THIRD_OF_REMAINDER))

    # Daughters Share
    @Rule(
        Daughters(P(lambda x: x == 1)), 
        Sons(P(lambda x: x == 0)),
        NOT(DaughtersShare())
    )
    def daughters_share_1(self):
        self.declare(DaughtersShare(HALF))
        self.shares.append(Share('daughters', HALF))

    @Rule(
        Daughters(P(lambda x: x >= 2)), 
        Sons(P(lambda x: x == 0)), 
        Daughters(MATCH.count),
        NOT(DaughtersShare())
    )
    def daughters_share_2(self, count):
        self.declare(DaughtersShare(TWO_THIRDS))
        self.shares.append(Share('daughters', TWO_THIRDS, count))

    @Rule(
        Daughters(P(lambda x: x > 0)), 
        Sons(P(lambda x: x > 0)), 
        Daughters(MATCH.count),
        NOT(DaughtersShare())
    )
    def daughters_share_3(self, count):
        self.declare(DaughtersShare(REMAINDER))
        self.shares.append(Share('daughters', REMAINDER, count))

    # Daughters Of Sons Share
    @Rule(
        Daughters(P(lambda x: x == 0)),
        DaughtersOfSons(P(lambda x: x == 1)),
        SonsOfSons(P(lambda x: x == 0)),
        NOT(DaughtersOfSonShare())
    )
    def daughters_of_sons_share_1(self):
        self.declare(DaughtersOfSonShare(HALF))
        self.shares.append(Share('daughters_of_sons', HALF))

    @Rule(
        Daughters(P(lambda x: x == 0)),
        DaughtersOfSons(P(lambda x: x >= 2)),
        SonsOfSons(P(lambda x: x == 0)),
        DaughtersOfSons(MATCH.count),
        NOT(DaughtersOfSonShare())
    )
    def daughters_of_sons_share_2(self, count):
        self.declare(DaughtersOfSonShare(TWO_THIRDS))
        self.shares.append(Share('daughters_of_sons', TWO_THIRDS, count))

    @Rule(
        DaughtersOfSons(P(lambda x: x > 0)), 
        Daughters(P(lambda x: x == 1)), 
        DaughtersOfSons(MATCH.count),
        NOT(DaughtersOfSonShare())
    )
    def daughters_of_sons_share_3(self, count):
        self.declare(DaughtersOfSonShare(ONE_SIXTH))
        self.shares.append(Share('daughters_of_sons', ONE_SIXTH, count))

    @Rule(
        DaughtersOfSons(P(lambda x: x > 0)), 
        SonsOfSons(P(lambda x: x > 0)), 
        DaughtersOfSons(MATCH.count),
        NOT(DaughtersOfSonShare())
    )
    def daughters_of_sons_share_4(self, count):
        self.declare(DaughtersOfSonShare(REMAINDER))
        self.shares.append(Share('daughters_of_sons', REMAINDER, count))
    
    # Full Sister Share
    @Rule(
        full_sisters_share_rules(),
        FullSister(P(lambda x: x == 1)),
        FullBrother(P(lambda x: x == 0)),
        NOT(FullSistersShare())
    )
    def full_sisters_share_1(self):
        self.declare(FullSistersShare(HALF))
        self.shares.append(Share('full_sisters', HALF))
    
    @Rule(
        full_sisters_share_rules(),
        FullSister(P(lambda x: x >= 2)),
        FullBrother(P(lambda x: x == 0)),
        FullSister(MATCH.count),
        NOT(FullSistersShare())
    )
    def full_sisters_share_2(self, count):
        self.declare(FullSistersShare(TWO_THIRDS))
        self.shares.append(Share('full_sisters', TWO_THIRDS, count))
    
    @Rule(
        FullSister(P(lambda x: x > 0)),
        FullBrother(P(lambda x: x == 0)),
        has_daughters_or_daughters_of_sons(),
        FullSister(MATCH.count),
        NOT(FullSistersShare())
    )
    def full_sisters_share_3(self, count):
        self.declare(FullSistersShare(REMAINDER))
        self.shares.append(Share('full_sisters', REMAINDER, count))

    @Rule(
        FullSister(P(lambda x: x > 0)),
        FullBrother(P(lambda x: x > 0)),
        FullSister(MATCH.count),
        NOT(FullSistersShare())
    )
    def full_sisters_share_4(self, count):
        self.declare(FullSistersShare(REMAINDER))
        self.shares.append(Share('full_sisters', REMAINDER, count))
    
    # Sister From Father Share
    @Rule(
        sisters_from_father_share_rules(),
        SisterFromFather(P(lambda x: x == 1)),
        BrotherFromFather(P(lambda x: x == 0)),
        NOT(SistersFromFatherShare())
    )
    def sisters_from_father_share_1(self):
        self.declare(SistersFromFatherShare(HALF))
        self.shares.append(Share('sisters_from_father', HALF))
    
    @Rule(
        sisters_from_father_share_rules(),
        SisterFromFather(P(lambda x: x >= 2)),
        BrotherFromFather(P(lambda x: x == 0)),
        SisterFromFather(MATCH.count),
        NOT(SistersFromFatherShare())
    )
    def sisters_from_father_share_2(self, count):
        self.declare(SistersFromFatherShare(TWO_THIRDS))
        self.shares.append(Share('sisters_from_father', TWO_THIRDS, count))
    
    @Rule(
        SisterFromFather(P(lambda x: x > 0)), 
        BrotherFromFather(P(lambda x: x == 0)),
        has_no_daughters(),
        has_no_daughters_of_sons(),
        FullSister(P(lambda x: x == 1)),
        SisterFromFather(MATCH.count),
        NOT(SistersFromFatherShare())
    )
    def sisters_from_father_share_3(self, count):
        self.declare(SistersFromFatherShare(ONE_SIXTH))
        self.shares.append(Share('sisters_from_father', ONE_SIXTH, count))
    
    @Rule(
        SisterFromFather(P(lambda x: x > 0)),
        BrotherFromFather(P(lambda x: x == 0)),
        FullSister(P(lambda x: x == 0)),
        has_daughters_or_daughters_of_sons(),
        SisterFromFather(MATCH.count),
        NOT(SistersFromFatherShare())
    )
    def sisters_from_father_share_4(self, count):
        self.declare(SistersFromFatherShare(REMAINDER))
        self.shares.append(Share('sisters_from_father', REMAINDER, count))
    
    @Rule(
        SisterFromFather(P(lambda x: x > 0)),
        BrotherFromFather(P(lambda x: x > 0)),
        SisterFromFather(MATCH.count),
        NOT(SistersFromFatherShare())
    )
    def sisters_from_father_share_5(self, count):
        self.declare(SistersFromFatherShare(REMAINDER))
        self.shares.append(Share('sisters_from_father', REMAINDER, count))
    
    # Brother Or Sister From Mother
    @Rule(
        OR(
            AND(
                BrotherFromMother(P(lambda x: x == 1)),
                SisterFromMother(P(lambda x: x == 0))
            ),
            AND(
                BrotherFromMother(P(lambda x: x == 0)),
                SisterFromMother(P(lambda x: x == 1))
            )
        ),
        NOT(BrothersAndSistersFromMotherShare())
    )
    def brother_or_sister_from_mother_share_1(self):
        self.declare(BrothersAndSistersFromMotherShare(ONE_SIXTH))
        self.shares.append(Share('brother_or_sister_from_mother', ONE_SIXTH))
    
    @Rule(
        OR(
            BrotherFromMother(P(lambda x: x > 0)),
            SisterFromMother(P(lambda x: x > 0))
        ),
        NOT(BrothersAndSistersFromMotherShare()),
        BrotherFromMother(MATCH.count_b),
        SisterFromMother(MATCH.count_s),
    )
    def brother_or_sister_from_mother_share_2(self, count_b, count_s):
        self.declare(BrothersAndSistersFromMotherShare(ONE_THIRD))
        self.shares.append(
            Share(
                'brother_or_sister_from_mother', 
                ONE_SIXTH, 
                count_b + count_s
            )
        )
    
    # Grandmother Share
    @Rule(
        MothersMother("alive"), 
        FathersMother("alive"),
        NOT(MothersMotherShare()),
        NOT(FathersMotherShare())
    )
    def mothers_mother_and_fathers_mother_share(self):
        self.declare(MothersMotherShare(ONE_TWELFTH))
        self.declare(FathersMotherShare(ONE_TWELFTH))
        self.shares.append(Share('mothers_mother', ONE_TWELFTH))
        self.shares.append(Share('fathers_mother', ONE_TWELFTH))

    @Rule(MothersMother("alive"), NOT(MothersMotherShare()))
    def mothers_mother_share(self):
        self.declare(MothersMotherShare(ONE_SIXTH))
        self.shares.append(Share('mothers_mother', ONE_SIXTH))

    @Rule(FathersMother("alive"), NOT(FathersMotherShare()))
    def fathers_mother_share(self):
        self.declare(FathersMotherShare(ONE_SIXTH))
        self.shares.append(Share('fathers_mother', ONE_SIXTH))
    
    # Grandfather Share
    @Rule(
        FathersFather("alive"), 
        has_heir_branch_only_boys(), 
        NOT(FathersFatherShare())
    )
    def fathers_father_share_1(self):
        self.declare(FathersFatherShare(ONE_SIXTH))
        self.shares.append(Share('fathers_father', ONE_SIXTH))

    @Rule(
        FathersFather("alive"), 
        has_heir_branch_only_girls(), 
        NOT(FathersFatherShare())
    )
    def fathers_father_share_2(self):
        self.declare(FathersFatherShare(REMAINDER_AND_ONE_SIXTH))
        self.shares.append(Share('fathers_father', REMAINDER_AND_ONE_SIXTH))

    @Rule(
        FathersFather("alive"), 
        has_no_heir_branch(), 
        AND(
            has_no_brothers_from_father(), 
            has_no_full_brother()
        ), 
        NOT(FathersFatherShare())
    )
    def fathers_father_share_3(self):
        self.declare(FathersFatherShare(REMAINDER))
        self.shares.append(Share('fathers_father', REMAINDER))

    # TODO: handle grandfather with brothers

    # Sons Share
    @Rule(
        Sons(P(lambda x: x > 0)), 
        Sons(MATCH.count),
        NOT(SonsShare())
    )
    def son_takes_the_rest(self, count):
        self.declare(SonsShare(REMAINDER))
        self.shares.append(Share('son', REMAINDER , count))

    # Sons Of Son Share
    @Rule(
        SonsOfSons(P(lambda x: x > 0)), 
        SonsOfSons(MATCH.count),
        NOT(SonsOfSonsShare())
    )
    def son_of_son_takes_the_rest(self, count):
        self.declare(SonsOfSonsShare(REMAINDER))
        self.shares.append(Share('son_of_son', REMAINDER , count))

    # Full Brother Share
    @Rule(
        FullBrother(P(lambda x: x > 0)), 
        FullBrother(MATCH.count),
        NOT(FullBrotherShare())
    )
    def full_brother_takes_the_rest(self, count):
        self.declare(FullBrotherShare(REMAINDER))
        self.shares.append(Share('full_brother', REMAINDER, count))

    # Brother From Father Share
    @Rule(
        BrotherFromFather(P(lambda x: x > 0)), 
        BrotherFromFather(MATCH.count),
        NOT(BrotherFromFatherShare())
    )
    def brother_from_father_takes_the_rest(self, count):
        self.declare(BrotherFromFatherShare(REMAINDER))
        self.shares.append(Share('brother_from_father', REMAINDER, count))

    # Son Of Full Brother Share
    @Rule(
        SonOfFullBrother(P(lambda x: x > 0)), 
        SonOfFullBrother(MATCH.count),
        NOT(SonOfFullBrotherShare())
    )
    def son_of_full_brother_takes_the_rest(self, count):
        self.declare(SonOfFullBrotherShare(REMAINDER))
        self.shares.append(Share('son_of_full_brother', REMAINDER, count))

    # Son Of Brother From Father Share
    @Rule(
        SonOfBrotherFromFather(P(lambda x: x > 0)), 
        SonOfFullBrother(MATCH.count),
        NOT(SonOfBrotherFromFatherShare())
    )
    def son_of_brother_from_father_takes_the_rest(self,count):
        self.declare(SonOfBrotherFromFatherShare(REMAINDER))
        self.shares.append(Share('son_of_brother_from_father', REMAINDER, count))

    # Full Uncle Share
    @Rule(
        FullUncle(P(lambda x: x > 0)), 
        FullUncle(MATCH.count),
        NOT(FullUncleShare())
    )
    def full_uncle_takes_the_rest(self, count):
        self.declare(FullUncleShare(REMAINDER))
        self.shares.append(Share('full_uncle', REMAINDER, count))

    # Uncle From Father Share
    @Rule(
        UncleFromFather(P(lambda x: x > 0)), 
        UncleFromFather(MATCH.count),
        NOT(UncleFromFatherShare())
    )
    def uncle_from_father_takes_the_rest(self, count):
        self.declare(UncleFromFatherShare(REMAINDER))
        self.shares.append(Share('uncle_from_father', REMAINDER, count))

    # Son Of Full Uncle Share
    @Rule(
        SonOfFullUncle(P(lambda x: x > 0)), 
        SonOfFullUncle(MATCH.count),
        NOT(SonOfFullUncleShare())
    )
    def son_of_full_uncle_takes_the_rest(self, count):
        self.declare(SonOfFullUncleShare(REMAINDER))
        self.shares.append(Share('son_of_full_uncle', REMAINDER, count))

    # Son Of Uncle From Father Share
    @Rule(
        SonOfUncleFromFather(P(lambda x: x > 0)), 
        SonOfUncleFromFather(MATCH.count),
        NOT(SonOfUncleFromFatherShare())
    )
    def son_of_uncle_from_father_takes_the_rest(self, count):
        self.declare(SonOfUncleFromFatherShare(REMAINDER))
        self.shares.append(Share('son_of_uncle_from_father', REMAINDER, count))

    """ End Sharing Rules """

    def print_shares(self):
        calculator = SharesCalculator(self.shares, self.amount)
        calculator.calculate()
