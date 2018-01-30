import pyhf
import numpy as np
import json

VALIDATION_TOLERANCE = 1e-7

def test_validation_1bin_shapesys():
    expected_result = {
        'obs': 0.450337178157,
        'exp': [
            0.06154653039922158,
            0.1472337570386738,
            0.3227412178815565,
            0.5995781547454528,
            0.8636787737204704
        ]
    }


    source = json.load(open('validation/data/1bin_example1.json'))
    pdf  = pyhf.hfpdf.hepdata_like(source['bindata']['sig'], source['bindata']['bkg'], source['bindata']['bkgerr'])
    data = source['bindata']['data'] + pdf.auxdata
    muTest = 1.0
    init_pars  = [1.0]*2 #mu + gam1
    par_bounds = [[0,10]] * 2
    clsobs, cls_exp = pyhf.runOnePoint(muTest, data,pdf,init_pars,par_bounds)[-2:]
    cls_obs = 1./clsobs
    cls_exp = [1./x for x in cls_exp]
    assert (cls_obs - expected_result['obs'])/expected_result['obs'] < VALIDATION_TOLERANCE
    for result,expected_result in zip(cls_exp, expected_result['exp']):
        assert (result-expected_result)/expected_result < VALIDATION_TOLERANCE


def test_validation_1bin_normsys():
    expected_result = {
        'obs': 0.0007930094233140433,
        'exp': [
            1.2529050370718884e-09,
            8.932001833559302e-08,
            5.3294967286010575e-06,
            0.00022773982308763686,
            0.0054897420571466075
        ]
    }
    source = {
      "binning": [2,-0.5,1.5],
      "bindata": {
        "data":    [120.0, 180.0],
        "bkg":     [100.0, 150.0],
        "sig":     [30.0, 95.0]
      }
    }
    spec = {
        'singlechannel': {
            'signal': {
                'data': source['bindata']['sig'],
                'mods': [
                    {
                        'name': 'mu',
                        'type': 'normfactor',
                        'data': None
                    }
                ]
            },
            'background': {
                'data': source['bindata']['bkg'],
                'mods': [
                    {
                        'name': 'bkg_norm',
                        'type': 'normsys',
                        'data': {'lo': 0.90, 'hi': 1.10}
                    }
                ]
            }
        }
    }
    pdf  = pyhf.hfpdf(spec)
    data = source['bindata']['data'] + pdf.auxdata

    muTest = 1.0
    init_pars  = [1.0, 0.0] #mu + alpha
    par_bounds = [[0,10],[-5,5]]
    clsobs, cls_exp = pyhf.runOnePoint(muTest, data,pdf,init_pars,par_bounds)[-2:]
    cls_obs = 1./clsobs
    cls_exp = [1./x for x in cls_exp]
    assert (cls_obs - expected_result['obs'])/expected_result['obs'] < VALIDATION_TOLERANCE
    for result,expected_result in zip(cls_exp, expected_result['exp']):
        assert (result-expected_result)/expected_result < VALIDATION_TOLERANCE


def test_validation_2bin_histosys():
    expected_result = {
        'obs': 0.09436700514736625,
        'exp': [
            8.131143652258812e-06,
            0.0001396307700293439,
            0.0020437905684851376,
            0.022094931468776054,
            0.14246926685789288,
        ]
    }
    source = json.load(open('validation/data/2bin_histosys_example2.json'))
    spec = {
        'singlechannel': {
            'signal': {
                'data': source['bindata']['sig'],
                'mods': [
                    {
                        'name': 'mu',
                        'type': 'normfactor',
                        'data': None
                    }
                ]
            },
            'background': {
                'data': source['bindata']['bkg'],
                'mods': [
                    {
                        'name': 'bkg_norm',
                        'type': 'histosys',
                        'data': {
                            'lo_hist': source['bindata']['bkgsys_dn'],
                            'hi_hist': source['bindata']['bkgsys_up'],
                        }
                    }
                ]
            }
        }
    }
    pdf  = pyhf.hfpdf(spec)
    data = source['bindata']['data'] + pdf.auxdata

    muTest = 1.0
    init_pars  = [1.0, 0.0] #mu + alpha
    par_bounds = [[0,10],[-5,5]]
    clsobs, cls_exp = pyhf.runOnePoint(muTest, data,pdf,init_pars,par_bounds)[-2:]
    cls_obs = 1./clsobs
    cls_exp = [1./x for x in cls_exp]
    assert (cls_obs - expected_result['obs'])/expected_result['obs'] < VALIDATION_TOLERANCE
    for result,expected_result in zip(cls_exp, expected_result['exp']):
        assert (result-expected_result)/expected_result < VALIDATION_TOLERANCE
