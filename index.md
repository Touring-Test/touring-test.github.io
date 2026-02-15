---
title: ""
layout: default
---
## Totals
{% assign total_miles = 0 %}
{% assign total_hours = 0 %}
{% assign total_tours = 0 %}
{% for post in site.posts %}
  {% assign total_miles = total_miles | plus: post.distance_traveld_NM %}
  {% assign total_hours = total_hours | plus: post.duration_h %}
  {% assign total_tours = total_tours | plus: 1 %}
{% endfor %}

| ---            | --:               | --             |
| Total Distance | {{ total_miles }} | nautical miles |
| Total Time     | {{ total_hours | divided_by: 24 | round: 0 }} | days
| Total #        | {{ total_tours }} | voyages |

## Tour Index

|Date|from|via|off- shore %|to |dist (NM)|time (hours)|avg speed (kn)|Crew|Skipper|Vessel|hyper- links|
|--- |--- |---|  :--:      |---| --:     | --:        | --:          |---|---|---|---| {%
 for post in site.posts %}
| [{{ post.date | date: "%Y-%m-%d" }}]({{ post.url | relative_url }}) | {{
 post.origin_locn         }} | {{ 
 post.via                 }} | {{ 
 post.offshore_percentage }} | {{ 
 post.terminus_locn       }} | {{ 
 post.distance_traveld_NM }} | {{ 
 post.duration_h          }} | {{ 
 post.distance_traveld_NM | times: 1.0 | divided_by: post.duration_h | round: 1 }} | {{
 post.crew                }} | {{
 post.skipper             }} | {{
 post.tags[0] | split: '_' | last }} | {%
 if post.gps_track %} [track]({{  post.gps_track | relative_url }}) {%
 endif %}{%
 if post.photos    %} [photos]({{ post.photos    | relative_url }}) {%
 endif %} | {%
 endfor %}
