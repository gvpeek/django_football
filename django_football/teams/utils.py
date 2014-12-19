from django.core.exceptions import ObjectDoesNotExist

import python_football

def create_playbook():
    playbook = Playbook(name='Basic',
                        plays=json.dumps(pickle.dumps(python_football.new_playbook())))
    playbook.save()

def initialize_cities():
    cities = []
    with open(os.path.join('football','csv_source_files','metroareas.csv'), 'r') as cities_file:
        cities_reader = csv.reader(cities_file,delimiter=',')
        for city in cities_reader:
            cities.append(City(name=city[0],
                               state = city[1],
                               pro = bool(int(city[2])),
                               semipro = bool(int(city[3])),
                               amateur = bool(int(city[4])),
                               region = city[5],
                               division = city[6],
                               )
                          )
    City.objects.bulk_create(cities)

def initialize_nicknames():
    nicknames = [] 
    with open(os.path.join('football','csv_source_files','nicknames.csv'), 'r') as nicknames_file:
        nickname_reader = csv.reader(nicknames_file,delimiter=',')
        for nickname in nickname_reader:
            nicknames.append(Nickname(name=nickname[0],
                                      pro = bool(int(nickname[1])),
                                      semipro = bool(int(nickname[2]))
                                      )
                             )
    Nickname.objects.bulk_create(nicknames)   

# TODO investigate better way of testing presence of data
def initialize_team_source_data():
    try:
        Playbook.objects.get(id=1)
    except ObjectDoesNotExist:
        create_playbook()
        
    try:
        City.objects.get(id=1)
    except ObjectDoesNotExist:
        initialize_cities()
        
    try:
        Nickname.objects.get(id=1)
    except ObjectDoesNotExist:
        initialize_nicknames()

def create_initial_universe_teams(universe, level):
    number_teams = determine_number_pro_teams(universe)
    if level == 'any':
        cities = City.objects.all()
        nicknames = Nickname.objects.all()
    elif level in ['pro', 'semipro', 'amateur']:
        level_filter = {}
        level_filter[level] = True
        cities = City.objects.filter(**level_filter)
        nicknames = Nickname.objects.filter(**level_filter)
    else:
        return HttpResponse("Invalid level for team creation.")
        
    coaches = [Coach(universe=universe,
                     first_name=names.first_name(),
                     last_name=names.last_name(),
                     skill=randint(60,90),
                     play_probabilities = json.dumps({}),
                     fg_dist_probabilities = json.dumps({})
                                       ) for x in xrange(int(number_teams))]
    for coach in coaches:
            coach.save()
    teams = [Team(universe=universe,
                  city=choice(cities),
                  nickname=choice(nicknames),
                  human_control=False,
                  home_field_advantage=randint(1,3),
                  draft_position_order = get_draft_position_order(),
                  coach = coaches.pop(),
                  playbook = Playbook.objects.get(id=1)) for x in xrange(int(number_teams))]
    Team.objects.bulk_create(teams)
