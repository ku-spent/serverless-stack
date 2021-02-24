from get_trends import get_thairath_trends


trends, source = get_thairath_trends()

assert(type(source) == str)
assert(type(trends) == list)
assert(len(trends) > 0)
assert(list(trends[0].keys()) == ['trend', 'topics'])

print(trends)

print("Test pass 🚀")
