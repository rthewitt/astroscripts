#DANGER: This currently points to thalamus!!!!
parietal-ip: 172.28.1.202
{% raw -%}
{% if grains['id'] == 'glial' %}
student-id: glial
{% endif %}
{%- endraw -%}
{%- for minion in minions -%}
{% raw %}
{% if grains['id'] == {% endraw %}'{{ minion[0] }}' {% raw %}%}{% endraw %}
student-id: {{ minion[1] }}
{% raw %}{% endif %}{% endraw %}
{%- endfor %}
