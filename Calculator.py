from constants import *
from fractions import Fraction
from Share import Share
from typing import List


class SharesCalculator():
    remainders: List[Share] = []
    fractions: List[Share] = []

    def __init__(self, shares: List[Share], amount: int):
        self.amount = amount
        self.filter_shares(shares)
    
    def filter_shares(self, shares: List[Share]):
        for share in shares:
            if isinstance(share.amount, Fraction):
                self.fractions.append(share)
            else:
                self.remainders.append(share)
    
    def calculate(self):
        amount = self.amount
        sum = 0
        
        # Calc the فروض shares
        for share in self.fractions:
            share.money = share.amount * amount
            sum += share.money
        
        # Calc the تعصيب shares
        for share in self.remainders:
            if share.amount == REMAINDER_AND_ONE_SIXTH:
                share.money = ONE_SIXTH * amount
                sum += share.money
            elif share.amount == ONE_THIRD_OF_REMAINDER:
                share.money = ONE_THIRD * (amount - sum)
                sum += share.money
        
        if sum > amount:
            mul_factor = float(amount / sum)
            for share in self.fractions:
                share.money *= mul_factor
            
            for share in self.remainders:
                if share.amount == REMAINDER_AND_ONE_SIXTH:
                    share.money *= mul_factor

        elif sum < amount:
            if len(self.fractions) == 1 and len(self.remainders) == 0:
                self.fractions[0].money = amount

            elif len(self.remainders) == 0:
                husband_or_wives_share = 0
                for share in self.fractions:
                    if(share.member_name == "wives" or share.member_name == "husband"):
                        husband_or_wives_share = share.money
                    
                new_amount = amount - husband_or_wives_share
                new_sum = sum - husband_or_wives_share
                mul_factor = float(new_amount / new_sum)

                for share in self.fractions:
                    if(share.member_name != "wives" and share.member_name != "husband"):
                        share.money *= mul_factor
                
            elif len(self.remainders) == 1:
                self.remainders[0].money += (amount - sum)

            else:
                omaryatanIsHere = False
                index = None
                for share in self.remainders:
                    if share.amount == ONE_THIRD_OF_REMAINDER:
                        omaryatanIsHere = True
                    else:
                        index = share

                if omaryatanIsHere:
                   index.money += (amount - sum)
                
                else:
                    girls_cnt = 0
                    boyes_cnt = 0
                    for share in self.remainders:
                        if (
                            share.amount == REMAINDER and (
                                share.member_name == "full_sisters" or 
                                share.member_name == "daughters" or 
                                share.member_name == "daughters_of_sons"
                            )
                        ):
                            girls_cnt = share.members_count
                        else:
                            boyes_cnt = share.members_count

                    girl_share = (amount - sum) / (2 * boyes_cnt + girls_cnt)

                    for share in self.remainders:
                        if (
                            share.amount == REMAINDER and (
                                share.member_name == "full_sisters" or 
                                share.member_name == "daughters" or 
                                share.member_name == "daughters_of_sons"
                            )
                        ):
                            share.money = girl_share * girls_cnt
                        else:
                            share.money = (2 * girl_share)  * boyes_cnt

        self.print_shares()

    def print_shares(self):
        print("------------------------------")
        for share in self.fractions:
            share.print_data()
            print("------------------------------")
        
        for share in self.remainders:
            share.print_data()
            print("------------------------------")


