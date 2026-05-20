import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path

plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 13,
    'axes.labelsize': 10,
    'figure.dpi': 180,
})

def savefig(name):
    plt.tight_layout()
    plt.savefig(f'figures/{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figures/{name}.png', bbox_inches='tight')
    plt.close()

# 1. Smooth continuum bump hunt
np.random.seed(2)
x=np.linspace(60,200,500)
bkg=1700*np.exp(-(x-60)/58)*(1+0.10*np.sin((x-60)/35))
z=420*np.exp(-0.5*((x-91)/9)**2)
h=180*np.exp(-0.5*((x-125)/8)**2)
y=bkg+z+h
obs=np.random.poisson(y)
fig,ax=plt.subplots(figsize=(7.2,4.2))
ax.step(x, y, where='mid', color='k', lw=1.2, label='data-like spectrum')
ax.plot(x,bkg,'--',color='#1f77b4',lw=2,label='smooth QCD continuum fit')
ax.fill_between(x,bkg,bkg+z,color='#999999',alpha=0.35,label=r'$Z\to b\bar b$ peak')
ax.fill_between(x,bkg+z,bkg+z+h,color='#d62728',alpha=0.45,label=r'$H\to b\bar b$ signal bump')
ax.axvspan(104,146,color='#d62728',alpha=0.08,label='Higgs window')
ax.axvspan(80,104,color='#2ca02c',alpha=0.08,label='sidebands')
ax.axvspan(146,200,color='#2ca02c',alpha=0.08)
ax.set_xlabel(r'$m_{bb}$ [GeV]')
ax.set_ylabel('Events / bin')
ax.set_title('Smooth continuum fit: CMS-style VBF H→bb multijet model')
ax.legend(frameon=False,fontsize=8,ncol=2)
ax.set_xlim(70,200); ax.set_ylim(0,None)
savefig('fig1_smooth_continuum_fit')

# 2. ABCD cartoon
fig,ax=plt.subplots(figsize=(5.2,4.8))
ax.set_xlim(0,2); ax.set_ylim(0,2)
colors={'A':'#d62728','B':'#ffbb78','C':'#98df8a','D':'#aec7e8'}
labels={
 'A':'A: signal region\npass x, pass y\nunknown QCD',
 'B':'B\npass x, fail y',
 'C':'C\nfail x, pass y',
 'D':'D\nfail x, fail y'
}
coords={'D':(0,0),'C':(0,1),'B':(1,0),'A':(1,1)}
for k,(i,j) in coords.items():
    ax.add_patch(Rectangle((i,j),1,1,facecolor=colors[k],alpha=0.35,edgecolor='k',lw=1.5))
    ax.text(i+0.5,j+0.55,labels[k],ha='center',va='center',fontsize=10,weight='bold' if k=='A' else None)
ax.axvline(1,color='k'); ax.axhline(1,color='k')
ax.set_xticks([0.5,1.5]); ax.set_xticklabels(['fail x','pass x'])
ax.set_yticks([0.5,1.5]); ax.set_yticklabels(['fail y','pass y'])
ax.set_title('ABCD method')
ax.text(1.0,-0.27,r'$N_A \simeq \kappa\,N_B N_C/N_D$',ha='center',fontsize=14)
ax.annotate('',xy=(1.55,1.02),xytext=(1.55,0.98),arrowprops=dict(arrowstyle='->'))
ax.annotate('',xy=(1.02,1.55),xytext=(0.98,1.55),arrowprops=dict(arrowstyle='->'))
for spine in ax.spines.values(): spine.set_visible(False)
savefig('fig2_abcd_method')

# 3. Pass/fail method
x=np.linspace(40,220,400)
fail=2200*np.exp(-(x-40)/70)*(1+0.07*np.cos(x/21))
r=0.08+0.0007*(x-100)+0.012*np.sin(x/35)
qcd_pass=fail*r
signal=35*np.exp(-0.5*((x-125)/9)**2)
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(7.2,5.2),sharex=True,gridspec_kw={'height_ratios':[2,1]})
ax1.plot(x,fail,color='#1f77b4',lw=2,label='fail region: QCD-rich data')
ax1.plot(x,qcd_pass,color='#ff7f0e',lw=2,label='predicted QCD in pass = fail × R(p/f)')
ax1.fill_between(x,qcd_pass,qcd_pass+signal,color='#d62728',alpha=0.45,label='possible signal in pass')
ax1.set_ylabel('Events')
ax1.set_title('Pass/fail or tag-rate method')
ax1.legend(frameon=False,fontsize=8)
ax2.plot(x,r,color='k',lw=2)
ax2.set_ylabel(r'$R_{p/f}$')
ax2.set_xlabel('mass or tagger-related observable')
ax2.text(120,max(r)*0.85,r'$N_{pass}^{QCD}(x)=R_{p/f}(x)N_{fail}^{QCD}(x)$',fontsize=12)
savefig('fig3_pass_fail_method')

# 4. Decorrelated classifier shared shape
x=np.linspace(70,200,300)
base=np.exp(-(x-70)/70)*(1+0.04*np.sin(x/18))
base=base/base.max()
fig,(a,b)=plt.subplots(1,2,figsize=(9,3.6),sharey=True)
for shift,c,l in [(0,'#1f77b4','low score'),(0.20,'#ff7f0e','medium score'),(-0.18,'#d62728','high score')]:
    sculpt=base*(1+shift*np.exp(-0.5*((x-125)/16)**2)-0.08*shift*np.exp(-0.5*((x-90)/12)**2))
    a.plot(x,sculpt/sculpt.max(),color=c,lw=2,label=l)
for c,l in [('#1f77b4','low score'),('#ff7f0e','medium score'),('#d62728','high score')]:
    a2=base*(1+0.015*np.sin(x/20))
    b.plot(x,a2/a2.max(),color=c,lw=2,label=l)
a.set_title('Ordinary classifier\ncan sculpt mass')
b.set_title('Adversarial / decorrelated classifier\nshared QCD shape')
for ax in (a,b):
    ax.axvline(125,color='k',ls=':',lw=1)
    ax.set_xlabel(r'$m_{bb}$ [GeV]')
    ax.legend(frameon=False,fontsize=8)
a.set_ylabel('Normalized QCD shape')
savefig('fig4_decorrelated_classifier')

# 5. fake factor loose tight flow
fig,ax=plt.subplots(figsize=(8.2,3.8)); ax.axis('off')
def box(x,y,w,h,text,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.04',facecolor=color,alpha=0.35,edgecolor='k'))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10)
def arrow(x1,y1,x2,y2,label=None):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='->',mutation_scale=15,lw=1.5,color='k'))
    if label: ax.text((x1+x2)/2,(y1+y2)/2+0.08,label,ha='center',fontsize=10)
box(0.05,0.55,0.22,0.28,'Loose / anti-tight\nfake-enriched data','#aec7e8')
box(0.39,0.55,0.22,0.28,'Measure fake factor\nFF = tight / anti-tight','#ffbb78')
box(0.73,0.55,0.22,0.28,'Predict tight SR\nfake yield + shape','#98df8a')
arrow(0.27,0.69,0.39,0.69)
arrow(0.61,0.69,0.73,0.69)
box(0.20,0.08,0.25,0.25,'Subtract prompt\ncontamination','#f7b6d2')
box(0.55,0.08,0.25,0.25,'Parameterize in\npT, η, jet multiplicity','#c7c7c7')
arrow(0.32,0.33,0.47,0.55)
arrow(0.68,0.33,0.54,0.55)
ax.set_title('Fake-factor / matrix-method logic for fake-object multijet backgrounds',fontsize=13)
ax.set_xlim(0,1); ax.set_ylim(0,1)
savefig('fig5_fake_factor_flow')

# 6. rebalance smear flow
fig,ax=plt.subplots(figsize=(8.2,3.6)); ax.axis('off')
steps=[('Low-MET\nmultijet data','#aec7e8'),('Rebalance jets\nforce pT balance','#ffbb78'),('Smear jets with\nresponse tails','#98df8a'),('Predict high-MET\nQCD tail','#d62728')]
xs=[0.04,0.29,0.54,0.79]
for (txt,col),x0 in zip(steps,xs): box(x0,0.45,0.18,0.28,txt,col)
for x1,x2 in zip([0.22,0.47,0.72],[0.29,0.54,0.79]): arrow(x1,0.59,x2,0.59)
ax.text(0.5,0.20,'Used when ordinary QCD enters the signal region through jet mismeasurement and fake missing transverse momentum.',ha='center',fontsize=10)
ax.set_title('Rebalance-and-smear method for QCD fake MET',fontsize=13)
ax.set_xlim(0,1); ax.set_ylim(0,1)
savefig('fig6_rebalance_smear')

print('wrote figures')
