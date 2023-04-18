
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookyb-ird'), ('-elephant','rele-vant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T)) # worst case scenario; insert all of T
    elif (T == ""):
        return(len(S)) # same idea
    else:
        if (S[0] == T[0]): 
            return(MED(S[1:], T[1:])) # ignore; move on to next letters
        else:
            #return(1 + min(MED(S, T[1:]), MED(S[1:], T))) # add 1 edit
            ins = MED(S,T[1:]) + 1
            dele = MED(S[1:], T) + 1
            sub = MED(S[1:],T[1:]) + 1
            return min(ins,dele,sub)
            # insertion: iterate through T, and if S does not contain, add 1 to S
            


def fast_MED(S, T, MED={}):
    if(S, T) in MED:
      return MED[(S,T)]
    
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S)) 
    else:
        if (S[0] == T[0]): 
            return(fast_MED(S[1:], T[1:])) # ignore; move on to next letters
        else:
            ins = fast_MED(S,T[1:]) + 1
            dele = fast_MED(S[1:], T) + 1
            sub = fast_MED(S[1:],T[1:]) + 1
            result = min(ins,dele,sub)
            # insertion: iterate through T, and if S does not contain, add 1 to S
    MED[(S,T)] = result # setting the value of the key (S,T) in the dictionary
    return result


def fast_align_MED(S, T, MED={}):
    return fast_align_MED_helper(S, T, MED={})[1][0], fast_align_MED_helper(S, T, MED={})[1][1]

def fast_align_MED_helper(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]
    
    if S == "":
        alignment = ["-" * len(T), T]
        return len(T), alignment
    elif T == "":
        alignment = [S, "-" * len(S)]
        return len(S), alignment
    else:
      if S[0] == T[0]:
        sub_dist, sub_alignment = fast_align_MED_helper(S[1:], T[1:], MED)
        alignment = [S[0] + sub_alignment[0], T[0] + sub_alignment[1]]
        return sub_dist, alignment
      else:
        ins_dist, ins_alignment = fast_align_MED_helper(S, T[1:], MED)
        del_dist, del_alignment = fast_align_MED_helper(S[1:], T, MED)
        sub_dist, sub_alignment = fast_align_MED_helper(S[1:], T[1:], MED)
    
        if ins_dist <= del_dist and ins_dist <= sub_dist:
          alignment = ["-" + ins_alignment[0], T[0] + ins_alignment[1]]
          return ins_dist + 1, alignment
        elif del_dist <= sub_dist:
          alignment = [S[0] + del_alignment[0], "-" + del_alignment[1]]
          return del_dist + 1, alignment
        else:
          alignment = [S[0] + sub_alignment[0], T[0] + sub_alignment[1]]
          return sub_dist + 1, alignment

      
def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        print(align_S, align_T)
        print(alignments[i][0],alignments[i][1])
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])


test_align()