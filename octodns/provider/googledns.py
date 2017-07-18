#
#
#

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from logging import getLogger

from google.cloud import dns
from oauth2client.client import GoogleCredentials

# from google.cloud.exceptions import NotFound

# from ..record import Record, Update
from .base import BaseProvider


# class GoogleAuthenticationError(Exception):
#
#     def __init__(self, data):
#         try:
#             message = data['errors'][0]['message']
#         except (IndexError, KeyError):
#             message = 'Authentication error'
#         super(CloudflareAuthenticationError, self).__init__(message)


class GoogleProvider(BaseProvider):
    '''
    Google DNS provider

    google:
        class: octodns.provider.googledns.GoogleProvider
    '''
    SUPPORTS_GEO = False
    # https://cloud.google.com/dns/overview#supported_dns_record_types
    SUPPORTS = set(('A', 'AAAA', 'CAA', 'CNAME', 'MX', 'NAPTR', 'NS', 'PTR',
                    'SOA', 'SPF', 'SRV', 'TXT'))
    MIN_TTL = 60
    TIMEOUT = 30

    def __init__(self, record, project_id, email, token, *args, **kwargs):
        self.log = getLogger('GoogleProvider[{}]'.format(id))
        self.log.debug('__init__: id=%s, email=%s, token=***', id, email)
        super(GoogleProvider, self).__init__(id, *args, **kwargs)

        self.credentials = GoogleCredentials.get_application_default()
        self.client = dns.Client(project=project_id,
                                 credentials=self.credentials)
        self.zones = None
        self.zone_records = {}

    def list_zones(self):
        if self.zones is None:
            zones = self.client.list_zones()
            return [zone.name for zone in zones]

    # def create_zone(self, name, dns_name, description):
    #     zone = self.client.zone(
    #         name,
    #         dns_name=dns_name,
    #         description=description
    #     )
    #     zone.create()
    #     return zone

    # def get_zone(project_id, name):
    #     client = dns.Client(project=project_id)
    #     zone = client.zone(name=name)

    #     try:
    #         zone.reload()
    #         return zone
    #     except NotFound:
    #         return None

    # def delete_zone(project_id, name):
    #     client = dns.Client(project=project_id)
    #     zone = client.zone(name)
    #     zone.delete()

    # def list_resource_records(project_id, zone_name):
    #     client = dns.Client(project=project_id)
    #     zone = client.zone(zone_name)

    #     records = zone.list_resource_record_sets()

    #     return [(record.name, record.record_type, record.ttl, record.rrdatas)
    #             for record in records]

    # def list_changes(project_id, zone_name):
    #     client = dns.Client(project=project_id)
    #     zone = client.zone(zone_name)

    #     changes = zone.list_changes()

    #     return [(change.started, change.status) for change in changes]

    # def create_command(args):
    #     """Adds a zone with the given name, DNS name, and description."""
    #     zone = create_zone(
    #         args.project_id, args.name, args.dns_name, args.description)
    #     print('Zone {} added.'.format(zone.name))

    # def get_command(args):
    #     """Gets a zone by name."""
    #     zone = get_zone(args.project_id, args.name)
    #     if not zone:
    #         print('Zone not found.')
    #     else:
    #         print('Zone: {}, {}, {}'.format(
    #             zone.name, zone.dns_name, zone.description))

    # def list_command(args):
    #     """Lists all zones."""
    #     print(list_zones(args.project_id))

    # def delete_command(args):
    #     """Deletes a zone."""
    #     delete_zone(args.project_id, args.name)
    #     print('Zone {} deleted.'.format(args.name))

    # def list_resource_records_command(args):
    #     """List all resource records for a zone."""
    #     records = list_resource_records(args.project_id, args.name)
    #     for record in records:
    #         print(record)
