#!/usr/bin/env python3

# import inspect
import random
import string
from toco.django.user import User, SessionToken, PasswordResetRequest

email='test@mail.com'
password='guest'

# u = User.load_with_auth(email, password)
        
# u.purge_sessions()
# token = u.get_new_session_token()
# print(token)
# print(token.user)
# # print(dir(token))
# # print(token.user_rel_toco_)
# token.test_attr = {'foo':'bar'}
# token.save()
# print(token.id)
# # del token.__dict__['user']
# # print(dir(token))
# token.reload()
# # token.add_relations()
# print(token)
# print(token.user)
# token.unroll_foreign_keys()
# print(token.user)

# print(dir(token))
# print(token.user_rel_toco_)

# request = PasswordResetRequest(email=email)
# request.create()
# print(User.load_from_password_reset_request(request).email)
# print(User.load_from_password_reset_request(request.id).email)

email = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)) + "@15xz22.com"
password = "guest"
u = User.new(email, password)
print(u.id)
u2 = User.from_email(email)
print(u2.id)
u3 = User.load_with_auth(email, password)
print(u3.id)
