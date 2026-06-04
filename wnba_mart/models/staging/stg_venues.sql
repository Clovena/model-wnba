select
distinct
"venue.id" as venue_id,
upper("venue.fullName") as venue_name,
upper("venue.address.city") as venue_city,
upper("venue.address.state") as venue_state,
concat(venue_city, ', ', venue_state) as venue_location,
"venue.indoor" as is_indoor_venue
from {{ source('raw', 'competitions') }}