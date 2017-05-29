
import nltk, re, pprint, csv, sqlite3
from nltk import word_tokenize
from urllib import request





def ai_grammar(input):
    text = word_tokenize(input)
    tags=nltk.pos_tag(text)

    # A TUPLIBÓL LISTÁT CSINÁLUNK, SZAVAK ÉS SZÓFAJOKKAL
    col1 = []
    col2 = []
    for i,j in tags:
        col1.append(i)
        col2.append(j)
    col1.append('.')
    col2.append('.')



# PHRASES




#SENTENCE ENUMERATION
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []
    temp = []
    i = 1
    for c in range(len(col1)):
        col3.append(i)
        col4.append('')
        col5.append('')
        col6.append('')
        col7.append('')
        temp.append('')
        temp[c] = col2[c]
        if col1[c] in '.': i += 1
        if col2[c] == 'NNS':
            col5[c] = 'Plur'
            col2[c] = 'NN'
        if col2[c] == 'NNP':
            col5[c] = 'Place'
            col2[c] = 'NN'
        if col2[c] in ('VBD','VBN', 'VBG', 'VBZ', 'VBP'):
            if col1[c] in ('is', 'am', 'are', 'has'): col2[c]='VB'
            if col2[c] in ('VBD'): col5[c] = 'Past'
            if col2[c] in ('VBN'): col7[c] += 'Perf'
            if col2[c] in ('VBG'): col7[c] = 'Cont'
            col2[c] = 'VB'
            if col5[c] == '' and col2[c] == 'VB': col5[c] = 'Pres'



# VERB TENSES
    for c in range(len(col1)-1):
        if col1[c] in ('will', 'shall', '\'ll') and col2[c+1] == 'VB':
            col5[c+1] = 'Fut'
            del col1[c], col2[c],  col3[c],  col4[c],  col5[c],  col6[c],  col7[c], temp[c]
            col1.append(' ')
            col2.append(' ')
            col3.append(' ')
            col4.append(' ')
            col5.append(' ')
            col6.append(' ')
            col7.append(' ')
            temp.append(' ')
    for c in range(len(col1)-1):
        if col1[c] in ('have', 'has', 'had', 'having', '\'d', '\'s') and col2[c+1] == 'VB' and (col5[c+1] in ('Past') or col7[c+1] in ('Perf', 'PerfCont')):
            #col7[c+1] = col7[c] + 'Perf'
            col5[c+1] = col5[c]
            del col1[c], col2[c],  col3[c],  col4[c],  col5[c],  col6[c],  col7[c], temp[c]
            col1.append(' ')
            col2.append(' ')
            col3.append(' ')
            col4.append(' ')
            col5.append(' ')
            col6.append(' ')
            col7.append(' ')
            temp.append(' ')
    for c in range(len(col1)-1):
        if col1[c] in ('be', 'being', 'am', 'is', 'are', 'was', 'were', 'been', '\'s') and col2[c+1] == 'VB' and (col5[c+1] in ('Past') or col7[c+1] in ('Perf', 'PerfCont')):
            col6[c+1] = 'Pass'
            col5[c+1]= col5[c]
            col7[c+1] = col7[c]
            del col1[c], col2[c],  col3[c],  col4[c],  col5[c],  col6[c],  col7[c], temp[c]
            col1.append(' ')
            col2.append(' ')
            col3.append(' ')
            col4.append(' ')
            col5.append(' ')
            col6.append(' ')
            col7.append(' ')
            temp.append(' ')
    for c in range(len(col1)-1):
        if col1[c] in ('be', 'being', 'am', 'is', 'are', 'was', 'were', 'been', '\'s') and col2[c+1] == 'VB' and col7[c+1] in ('Cont', 'PerfCont'):
            col7[c+1] += col7[c] + 'Cont'
            col5[c+1] = col5[c]
            del col1[c], col2[c],  col3[c],  col4[c],  col5[c],  col6[c],  col7[c], temp[c]
            col1.append(' ')
            col2.append(' ')
            col3.append(' ')
            col4.append(' ')
            col5.append(' ')
            col6.append(' ')
            col7.append(' ')
            temp.append(' ')
    for c in range(len(col1)-1):
        if col1[c] in ('can', 'could', 'should', 'must', 'may','might', '\'d') and col2[c+1] == 'VB':
            col7[c+1] += col1[c]
            del col1[c], col2[c],  col3[c],  col4[c],  col5[c],  col6[c],  col7[c], temp[c]
            col1.append(' ')
            col2.append(' ')
            col3.append(' ')
            col4.append(' ')
            col5.append(' ')
            col6.append(' ')
            col7.append(' ')
            temp.append(' ')



    #RULES
    for c in range(len(col1)): # VB: VP
        if col2[c] in ('VB'):
            col4[c] = 'VP'
    for c in range(len(col1)-2): # DT/JJ + JJ + NN or DT + NUM + NN
        if (col2[c] in ('DT', 'JJ')  and col2[c+1] in 'JJ' and col2[c+2] in 'NN') or (col2[c] in 'DT' and col2[c+1] in 'CD' and col2[c+2] in 'NN'):
            col4[c] = 'NP'
            col4[c+1] = 'NP'
            col4[c+2] = 'NP'
    for c in range(len(col1)-1): # DT + NN
        if col2[c] in ('DT')  and col2[c+1] in 'NN' and col4[c] == '':
            col4[c] = 'NP'
            col4[c+1] = 'NP'
    for c in range(len(col1)-1): # JJ + NN
        if col2[c] in ('JJ','CD')  and col2[c+1] in 'NN' and col4[c] == '':
            col4[c] = 'NP'
            col4[c+1] = 'NP'
    for c in range(len(col1)-1): #VB + DT: első szó az biztos VP
        if col2[c] in ('VB')  and col2[c+1] in 'DT' and col4[c] == '':
            col4[c] = 'VP'
    for c in range(len(col1)): # NN, ha még nincs besorolva: NP
        if col2[c] in ('NN')  and col4[c] == '':
            col4[c] = 'NP'
    for c in range(len(col1)):
        if col2[c] in ('VB')  and col4[c] == '':
            col4[c] = 'VP'
    for c in range(len(col1)-2):
        if col4[c] in ('VP')  and col2[c+1] in 'IN' and col4[c] == '':
            col4[c+1] = col4[c+2]
    for c in range(len(col1)-2):# NN/JJ + and/or/, + NN/JJ
        if col1[c+1] in ('or', 'and', ',')  and ((col2[c] in 'NN' and col2[c+2] in 'NN') or (col2[c] in 'JJ' and col2[c+2] in 'JJ') ):
            col4[c] = 'NP'
            col4[c+1] = 'NP'
            col4[c+2] = 'NP'







    v_nr = []
    nr = []
    vpnp = []
    vpnp2 = []
    verb_row = []
    who = []
    who_adj = []
    do = []
    what = []
    what_adj = []
    how = []
    v_count = 0
    text_out=[]
    for c in range(len(col1)):
        v_nr.append('')
        who.append('')
        who_adj.append('')
        do.append('')
        how.append('')
        what.append('')
        what_adj.append('')
        vpnp.append('')
        vpnp2.append('')
        verb_row.append('')
        nr.append(v_count)
        v_count += 1
        #text_out.append('')


    # A TÖBBIGÉS MONDATOKNÁL KERESSÜK  A MONDATHATÁROKAT: VESSZŐ, VAGY KIFEJEZÉS: but, altough, etc
    v_count=0
    for c in range(len(col1)-1):
        if col4[c] == 'VP': v_count += 1 # számolja az igéket...
        if col1[c] != ' ': v_nr[c] = v_count # majd kiírja. (kivéve a végén az üres cellákat)
        if col3[c] != col3[c+1]: v_count = 0 #új mondatnál újraindul az igeszámolás

    #for c in range(len(col1)): #visszafele kezdi el nézni...
        #if col1[c] != ' ' and int(v_nr[c]) > 1 and col1[c] in (',',';'): col2[c] = '.' # ha több ige is van a mondatban, akkor a vesszők is mondathatárok

    i = 1
    for c in range(len(col1)): # újraszámozzuk a mondatokat
        if col1[c] != ' ': col3[c] = i #(kivéve a végén az üres cellákat)
        if col2[c] in '.': i += 1

    for c in range(len(col1)-1):
        if col4[c] == 'VP': v_count += 1 # számolja az igéket...
        if col1[c] != ' ': v_nr[c] = v_count # majd kiírja. (kivéve a végén az üres cellákat)
        if col3[c] != col3[c+1]: v_count = 0 #új mondatnál újraindul az igeszámolás





    # MEGHATÁROZZUK, HOGY MELYIK A MAIN ILL. ADJ AZ NP-K KÖZÜL
    for c in range(len(col1)-2): # újraszámozzuk a mondatokat
        if col4[c] == 'NP' and col2[c+1] in ('IN','POS') and col4[c] == 'NP' and vpnp[c] != 'main':
            i=0
            while col4[c-i] == 'NP':
                if col1[c+1] ==  '\'s': vpnp[c-i] = 'adj'
                else: vpnp[c-i] = 'main'
                i+=1
            i=2
            vpnp[c+1] = 'adj'
            while col4[c+i] == 'NP':
                if col1[c+1] == '\'s': vpnp[c+i] = 'main'
                else: vpnp[c+i] = 'adj'
                i+=1






    # WHO - DOes - WHAT


    # WHO - DO
    for c in range(len(col4)):
        if col4[c] == 'VP':
            do[c] = col1[c]
            vpnp2[c] = 'do'
            i = 1
            while col4[c-i] != 'VP' and col1[c-i] != '.' and i <= c:
                #who[c-i] = 'x'
                if col4[c-i] == 'NP' and col2[c-i] == 'NN' and vpnp[c-i] in ('main', ''):
                    if col6[c] == 'Pass':
                        what[c-i] = col1[c-i]
                        vpnp2[c-i] = 'what'
                        if col1[c+1] != 'by':
                            who[c-i] = 'someone'
                            vpnp2[c-i] = 'who'
                        #what[c] += col1[c-i]
                        #who[c] += 'someone'
                        verb_row[c-i] = str(c)
                    if col6[c] != 'Pass':
                        who[c-i] = col1[c-i]
                        vpnp2[c-i] = 'who'
                        #who[c] += col1[c-i]
                        verb_row[c-i] = str(c)
                i += 1

    # WHAT
    for c in range(len(col4)-1):
        if col4[c] == 'VP':
            i = 1
            while (col4[c+i] != 'VP' and col1[c+i] != '.' and c+i < len(col4) and who[c+i] == '' ):
                #what[c+i] = 'y'
                if (col4[c+i] == 'NP' and col2[c+i] == 'NN') or (col2[c+i] == 'PRP' or col1[c+i] == 'that' or col1[c+i] == 'it') and vpnp[c+i] in ('main', ''):
                    if col6[c] != 'Pass':
                        what[c+i] = col1[c+i]
                        vpnp2[c+i] = 'what'
                    if col6[c] == 'Pass' and col1[c+1] == 'by':
                        who[c+i] = col1[c+i]
                        vpnp2[c+i] = 'who'
                        
                        #what[c] += col1[c+i]
                        verb_row[c+i] = str(c)
                i += 1

    #HOW
    for c in range(len(col4)-1):
        if col4[c] == 'VP':
            i = 1
            while (col4[c+i] != 'VP' and col1[c+i] != '.' and c+i < len(col4) and who[c+i] == '' ):
                if (col2[c+i] == 'JJ' or col2[c+i] == 'RB') and col4[c+i] != 'NP':
                    how[c+i] = col1[c+i]
                    vpnp2[c+i] = 'how'
                    #how[c] += col1[c+i]
                    verb_row[c+i] = str(c)
                i += 1







    # megszámolni a mondaton belüli VP-t, ha 1, akkor ok, ha több, akkor kérdőjeles. EZT EGYELŐRE NEM HASZNÁLJUK KI!!
    # Keresni a veszzőket, but, however, though, stb EZZEL MÉG KIEGÉSZÍTENI!
    # WHEN, WHERE RÉSZEKET AZONOSÍTANI!
    # IDŐ ÉS HELYHATÁROZÓK AZONOSÍTÁSA, MÉG A MAIN/ADJ NP ELŐTT


    # DONE:
    # PHRASE: AS ... AS, FOR THE XXX


    #PRINT COLUMNS

#    for c in range(len(col1)):
    text_out=(nr, col1,col2, col3, col4, v_nr, vpnp, vpnp2, who, do, what, how, verb_row)
        #text_out[c] += (str(nr[c]) + '    ' + col1[c] + ' '*(15-len(col1[c])) + col2[c] + ' '*(6-len(col2[c])) + str(col3[c]) + '  ' + col4[c] + ' '*(6-len(col4[c])) + '     ' + str(v_nr[c]) + '  ' + vpnp[c] + ' '*(6-len(vpnp[c])) + vpnp2[c] + ' '*(6-len(vpnp2[c])) + who[c] + ' '*(10-len(who[c])) + do[c] + ' '*(10-len(do[c])) + what[c]+ ' '*(10-len(what[c])) + how[c]+ ' '*(10-len(how[c])) + verb_row[c])

#print(text_out)
    return (text_out)
