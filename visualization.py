"""Dependency-free schematic SVG export, not a geographic map."""
import math
from html import escape

def export_svg(s,path):
    from routing import validate
    validate(s);nodes=s['nodes'];n=len(nodes)
    points={x:(420+280*math.cos(2*math.pi*i/n-math.pi/2),350+260*math.sin(2*math.pi*i/n-math.pi/2)) for i,x in enumerate(nodes)}
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="840" height="740" viewBox="0 0 840 740">','<rect width="840" height="740" fill="#f4f6f1"/>','<g font-family="Arial,sans-serif"><text x="30" y="35" font-size="23" fill="#24483e">Relief Route — road network</text><text x="30" y="61" font-size="12">Schematic only • distances in km • dashed red = blocked road</text>']
    for e in s['roads']:
        x,y=points[e['u']];a,b=points[e['v']];blocked=e.get('blocked',False)
        out.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="{"#bc5148" if blocked else "#b0bdb3"}" stroke-width="2"'+(' stroke-dasharray="7 5"' if blocked else '')+'/>')
        out.append(f'<text x="{(x+a)/2}" y="{(y+b)/2}" font-size="11" fill="#334a41" paint-order="stroke" stroke="#f4f6f1" stroke-width="4">{e["distance"]:g}</text>')
    for name,(x,y) in points.items():
        color='#d48536' if name==s['depot'] else '#245a47' if name in s['deliveries'] else '#78857d'
        out.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{color}"/><text x="{x}" y="{y+34}" text-anchor="middle" font-size="13" fill="#153b2f" paint-order="stroke" stroke="#f4f6f1" stroke-width="3">{escape(name)}</text>')
    out.append('<text x="30" y="716" font-size="12">Orange: depot • Green: delivery • Grey: transit node • Synthetic study, not operational guidance</text></g></svg>')
    path.write_text('\n'.join(out))
