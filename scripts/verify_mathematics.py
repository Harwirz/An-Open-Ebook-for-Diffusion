"""Independent low-dimensional checks for the ebook's algebra.

These are formula checks, not image-generation experiments or training results.
"""
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(20261009)
results = {}

def require(name, error, tolerance=1e-10):
    error = float(error)
    if not error < tolerance:
        raise AssertionError(f'{name}: error={error}, tolerance={tolerance}')
    results[name] = {'max_absolute_error': error, 'tolerance': tolerance, 'passed': True}

# DDPM posterior via generic joint-Gaussian conditioning, independently of
# the precision/completing-the-square derivation in the prose.
errors = []
for _ in range(500):
    previous = rng.uniform(.001, .999)
    beta = rng.uniform(.001, .2)
    alpha = 1-beta
    cumulative = previous*alpha
    x0, xk = rng.normal(size=2)
    prior_mean = np.sqrt(previous)*x0
    prior_var = 1-previous
    covariance = np.sqrt(alpha)*prior_var
    observation_var = alpha*prior_var+beta
    mean_conditioned = prior_mean+covariance/observation_var*(xk-np.sqrt(alpha)*prior_mean)
    var_conditioned = prior_var-covariance**2/observation_var
    mean_book = np.sqrt(previous)*beta/(1-cumulative)*x0+np.sqrt(alpha)*(1-previous)/(1-cumulative)*xk
    var_book = beta*(1-previous)/(1-cumulative)
    errors.extend([abs(mean_book-mean_conditioned),abs(var_book-var_conditioned)])
require('DDPM posterior from joint Gaussian', max(errors))

# Orthogonal v conversion and conditional derivative in angular time.
x0, eps = rng.normal(size=(2, 1000, 3))
angles = rng.uniform(.00001, np.pi/2-.00001, size=(1000,1))
a, b = np.cos(angles), np.sin(angles)
xt, v = a*x0+b*eps, a*eps-b*x0
require('v parameterization inverse',max(np.max(abs(a*xt-b*v-x0)), np.max(abs(b*xt+a*v-eps))))

# VP probability flow recovered through the general Gaussian-path velocity.
t = np.linspace(.0001,.9999,1000)
beta = 2.3
a = np.exp(-beta*t/2)
b = np.sqrt(1-a*a)
ap = -beta*a/2
bp = beta*a*a/(2*b)
coefficient = ap/a*b*b-b*bp
require('Gaussian path to VP half coefficient',np.max(abs(coefficient+beta/2)))

# Conditional expectation CFM for arbitrary Gaussian endpoints; compare it
# to a derivative of the analytically correct marginal transport map.
tau = np.linspace(.001,.999,1000)
m, c, z = 1.7, .6, -.83
h = (1-tau)**2+c*tau*tau
hp = -2*(1-tau)+2*c*tau
y = tau*m+np.sqrt(h)*z
conditional = m+(tau*c-(1-tau))/h*(y-tau*m)
transport_derivative = m+hp/(2*np.sqrt(h))*z
require('Gaussian CFM to marginal transport',np.max(abs(conditional-transport_derivative)))

# CNF likelihood sign via an explicit scaling map in dimension d.
d, rate = 5, .4
x = rng.normal(size=(100, d))
y = np.exp(rate)*x
logp0 = -.5*np.sum(x*x,axis=1)-d/2*np.log(2*np.pi)
logp1 = -.5*np.sum((y/np.exp(rate))**2,axis=1)-d/2*np.log(2*np.pi)-d*rate
require('CNF divergence integral sign',np.max(abs(logp1+d*rate-logp0)))

# Same-marginal stationary VP: PF velocity must vanish, while the
# reverse-SDE drift is nonzero for nonzero x.
x = rng.normal(size=(100,3))
f = -beta*x/2
score = -x
require('Stationary Gaussian probability flow',np.max(abs(f-beta*score/2)))

out = Path(__file__).resolve().parents[1]/'qa'/'mathematics-checks.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':len(results),'passed':all(r['passed'] for r in results.values())}))
