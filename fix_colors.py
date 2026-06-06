import os

file_path = r"d:\Helping Hand College Work\Helping Hand College\templates\core\dashboard_patient.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    # Main wrappers
    'bg-white rounded-2xl border border-surface-200 shadow-sm': 'card',
    'bg-white rounded-2xl max-w-md': 'glass max-w-md',
    
    # Text colors
    'text-navy-900': 'text-white',
    'text-navy-800': 'text-slate-200',
    'text-navy-600': 'text-white',
    'text-navy-500': 'text-white',
    'text-surface-600': 'text-slate-400',
    'text-surface-500': 'text-slate-400',
    'text-surface-400': 'text-slate-500',
    'text-surface-300': 'text-slate-500',
    
    # Inner cards
    'bg-surface-50 border border-surface-200': 'bg-white/5 border border-white/10',
    'bg-surface-50/50 border border-surface-200': 'bg-white/5 border border-white/10',
    'bg-surface-200': 'bg-white/10',
    'bg-surface-50': 'bg-transparent',
    
    # Badges / Inner containers
    'bg-navy-50 border border-navy-100': 'bg-blueGlow/10 border border-blueGlow/20',
    'bg-navy-900 rounded-2xl p-6 text-white border border-navy-800 shadow-md': 'card',
    'bg-navy-800 p-3 rounded-xl border border-navy-700': 'bg-white/5 p-3 rounded-xl border border-white/10',
    
    # Yellows to terracottas / blueglows
    'bg-saffron-500': 'bg-blueGlow',
    'text-saffron-500': 'text-blueGlow',
    'text-saffron-600': 'text-terracotta',
    'hover:text-saffron-700': 'hover:text-white',
    'bg-saffron-50': 'bg-terracotta/10',
    'border-saffron-200': 'border-terracotta/20',
    'border-saffron-100': 'border-terracotta/20',
    'text-saffron-800': 'text-terracotta',
    'text-saffron-400': 'text-blueGlow',
    'from-saffron-500 to-saffron-600': 'from-maroon to-terracotta',
    
    # Greens
    'bg-flaggreen-500': 'bg-terracotta',
    'text-flaggreen-600': 'text-terracotta',
    'bg-flaggreen-50 border border-flaggreen-100': 'bg-terracotta/10 border border-terracotta/20',
    
    # Reds
    'text-red-500': 'text-red-400',
    'hover:bg-red-50': 'hover:bg-red-500/10',
    'border-red-200/60': 'border-red-500/20',
    'bg-red-50': 'bg-red-500/10',
    'text-red-600': 'text-red-400',
    'border-red-100': 'border-red-500/20',
    
    # Modal
    'bg-navy-900 text-white flex items-center justify-between border-b border-navy-800': 'bg-[#081120] text-white flex items-center justify-between border-b border-white/10',
    'border-surface-100': 'border-white/10',
    'border-surface-200': 'border-white/10',
    'border-surface-300': 'border-white/10',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Dashboard colors updated successfully.")
