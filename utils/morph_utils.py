import pandas as pd

def getGreekRoles():
    return list(morphCodeLocalizationMapGrk[2].keys())

# // These reflect the columns on page 55 of https://greekcntr.org/downloads/project.pdf
# // This helps us translate codes starting and the 3rd place (the 2nd index) of a morph string
# // The numbered keys are the index of that code in the string, where the letter index is the code
# // Each role's 3rd index (the type code) is different, so we nest index 3 in the role's entry

morphCodeLocalizationMapGrk = {
    2: { #// role
        'N': {
            'key': 'noun',
            3: { #// noun types
                'S': 'substantive_adj',
                'P': 'predicate_adj',
            },
        },
        'A': {
            'key': 'adjective',
            3: { #// adjective types
                'A': 'ascriptive',
                'R': 'restrictive',
            },
        },
        'E': {
            'key': 'determiner',
            3: { #// determiner types
                'A': 'article',
                'D': 'demonstrative',
                'F': 'differential',
                'P': 'possessive',
                'Q': 'quantifier',
                'N': 'number',
                'O': 'ordinal',
                'R': 'relative',
                'T': 'interrogative',
            },
        },
        'R': {
            'key': 'pronoun',
            3: { #// pronoun types
                'D': 'demonstrative',
                'P': 'personal',
                'E': 'reflexive',
                'C': 'reciprocal',
                'I': 'indefinite',
                'R': 'relative',
                'T': 'interrogative',
            },
        },
        'V': {
            'key': 'verb',
            3: { #// verb types
                'T': 'transitive',
                'I': 'intransitive',
                'L': 'linking',
                'M': 'modal',
                'P': 'periphrastic',
            },
        },
        'I': {
            'key': 'interjection',
            3: { #// interjection types
                'E': 'exclamation',
                'D': 'directive',
                'R': 'response',
            },
        },
        'P': {
            'key': 'preposition',
            3: { #// preposition types
                'I': 'improper',
            },
        },
        'D': {
            'key': 'adverb',
            3: { #// adverb types
                'O': 'correlative',
            },
        },
        'C': {
            'key': 'conjunction',
            3: { #// conjuction types
                'C': 'coordinating',
                'S': 'subordinating',
                'O': 'correlative',
            },
        },
        'T': {
            'key': 'particle',
            3: { #// particle types
                'F': 'foreign',
                'E': 'error',
            },
        },
    },
    4: { #// mood
        'I': 'indicative',
        'M': 'imperative',
        'S': 'subjunctive',
        'O': 'optative',
        'N': 'infinitive',
        'P': 'participle',
    },
    5: { #// tense
        'P': 'present',
        'I': 'imperfect',
        'F': 'future',
        'A': 'aorist',
        'E': 'perfect',
        'L': 'pluperfect',
    },
    6: { #// voice
        'A': 'active',
        'M': 'middle',
        'P': 'passive',
    },
    7: { #// person
        1: 'first',
        2: 'second',
        3: 'third',
    },
    8: { #// case
        'N': 'nominative',
        'G': 'genitive',
        'D': 'dative',
        'A': 'accusative',
        'V': 'vocative',
    },
    9: { #// gender
        'M': 'masculine',
        'F': 'feminine',
        'N': 'neuter',
    },
    10: { #// number
        'S': 'singular',
        'P': 'plural',
    },
    11: { #// other
        'C': 'comparative',
        'S': 'superlatives',
        'D': 'diminutive',
        'I': 'indeclinable',
    },
}

morphFields = [ 'role','type','mood','tense','voice','person','case','gender','number']

def findRoleNameForCharGreek(char):
    roles = morphCodeLocalizationMapGrk[2]
    if char in roles.keys():
        return roles[char]['key']
    print(f"findRoleNameForCharGreek - key not found for {char}")
    return None

def getIndexForChar(char):
    num = ord(char)
    if (char >= 'A') and (char <= 'Z'):
        num = num - ord('A') + 11
    elif (char >= '0') and (char <= '9'):
        num = num - ord('0')
    elif (char >= 'a') and (char <= 'z'):
        num = num - ord('a') + 41
    else:
        if char != ',':
            print(f"getIndexForChar - unexpected character '{char}'")
        num = -1
    return num

def getCharForIndex(num):
    if (num >=0) and (num < 10):
        char = chr(ord('0') + num)
    elif (num >= 11) and (num < (11 + 26)):
        char = chr(ord('A') + (num - 11))
    elif (num >= 41) and (num < (41 + 26)):
        char = chr(ord('a') + (num - 41))
    elif num == -1:
        char = ','
    else:
        print(f"getCharForIndex - unexpected value '{num}'")
        char = '?'
    return char

def getChar(string, idx):
    return string[idx:idx+1]

def morphToDict(morph):
    results = {
        'morph': morph
    }

    # parse all the fields
    for i in range(len(morphFields)):
        field = morphFields[i]
        char = getChar(morph, 3 + i)
        results[field + '_key'] = char
        results[field] = getIndexForChar(char)
    return results

def extract(text, match, start, end):
    subStr = text[start:end]
    if (subStr == match):
        return True
    else:
        return False

def filterSyntacticalRole(sequence, role):
    def filterFunc(variable):
        results = extract(variable, role, 3, 4)
        return results

    filtered = filter(filterFunc, sequence)
    return filtered

def findFieldsForRole(unique_morph_list, role):
    field_data = {}
    print(f"\nFor role: '{role}'")

    role_list = list(filterSyntacticalRole(unique_morph_list, role))

    role_dict =  list(map(morphToDict, role_list))

    role_frame = pd.DataFrame(role_dict)

    for field in morphFields:
        field_key = field + '_key'
        field_frequency = role_frame[field_key].value_counts()
        print(f"\nFor '{role}' - instances of '{field}':")
        # print(field_frequency)
        field_list = list(dict(field_frequency).keys())
        print(field_list)
        field_list.sort()
        field_data[field] = field_list
    return field_data

def findFieldsFrequencyForRole(unique_morph_list, role):
    field_data = {}
    print(f"\nFor role: '{role}'")

    role_list = list(filterSyntacticalRole(unique_morph_list, role))

    role_dict =  list(map(morphToDict, role_list))

    role_frame = pd.DataFrame(role_dict)

    for field in morphFields:
        field_key = field + '_key'
        field_frequency = role_frame[field_key].value_counts()
        role_name = f"{findRoleNameForCharGreek(role)} ({role})"
        print(f"\nFor '{role_name}' - frequency of '{field}':")
        print(field_frequency)
        field_data[field] = field_frequency
    return field_data
