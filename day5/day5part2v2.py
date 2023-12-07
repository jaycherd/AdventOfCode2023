from icecream import ic
import re
from typing import Set,Optional,List,Tuple









"""
XXX idea XXX
second idea, i know my logic in v1 is sound however it is adding up to negative nums which is impossible, not sure why atm, may look later
so my new idea, is to start from the end, that is start from the min location and try to work my way up to a seed that is valid, aka a seed num
that is within one of the beginning seed intervals, to do this i think it could be much simpler, that is, we start by getting all
end locations then, we start with the smallest location value and work our way up, idk still, would be annoying to read file in reverse tho too

turns out most people having issues with this, so im not alone, and i think v1 is on the right track i dont think above logic is as feasible"""