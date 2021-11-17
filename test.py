import os
import shutil
import copy

class oh:
    def __init__(self):
        self.xxx = 10
class wtf:
    def __init__(self):
       self.a = 5
       self.vl = oh()

x = wtf()
y = copy.deepcopy(x)
x.vl.xxx -=1 
print(x.vl.xxx, y.vl.xxx)
# for virus in ['blue-rim-light', 'classic', 'green', 'red-rim-light']:
#     os.mkdir('sprites/enemies/' + virus)
#     for file_name in os.listdir(virus):
#         name = file_name.split('_')[-1]
#         if name[0] == '0' and name[1] != '.':
#             name = name[1:]
#         img_type = file_name.split('_')[0].split('-')[-1].title()
#         if not os.path.exists('sprites/enemies/' + virus + '/' + img_type):
#             os.mkdir('sprites/enemies/' + virus + '/' + img_type)
#         shutil.copy(f'{virus}/{file_name}', f'sprites/enemies/{virus}/{img_type}/{name}')
# for status in ['Attack', 'Death', 'Hurt', 'Idle', 'Run']:
#     for i, file_name in enumerate(os.listdir('sprites/enemies/zom4/' + status)):
#         os.rename('sprites/enemies/zom4/' + status + '/' + file_name, 'sprites/enemies/zom4/' + status + '/' + f'{i}.png')