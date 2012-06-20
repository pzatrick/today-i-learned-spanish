from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy 
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from tutorial.security import groupfinder

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, 
                          root_factory='tutorial.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_card', '/view_card/{cardid}')
    config.add_route('add_card', '/add_card/{cardid}')
    config.add_route('edit_card', '/{cardid}/edit_card')
    config.include("pyramid_haml")
    config.scan()
    return config.make_wsgi_app()

