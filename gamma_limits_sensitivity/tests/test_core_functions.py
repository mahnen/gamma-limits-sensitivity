'''
This is a set of test in order to check the
core functions
'''
import gamma_limits_sensitivity as gls
import numpy as np
from scipy import integrate

from helper_functions_for_tests import get_a_eff_list


def test_get_energy_range():
    '''
    Test if the function really returns sensible energy ranges
    in units of TeV
    '''
    a_eff_list = get_a_eff_list()

    for a_eff in a_eff_list:
        e_range = gls.get_energy_range(a_eff)
        assert e_range[0] > 0.05  # all supplied effective areas start > 50 GeV
        assert e_range[1] < 100   # all supplied effective areas stop < 100 TeV


def test_f_0_gamma_mesh():
    '''
    Test if the phase space box makes sense
    '''
    f_0_test = 1e-12
    gamma_test = -2.6

    f_0_lim, gamma_lim = gls.get_f_0_gamma_limits(f_0_test, gamma_test)
    f_0_mesh, gamma_mesh = gls.get_f_0_gamma_mesh(
        f_0_lim,
        gamma_lim,
        pixels_per_line=30)

    assert f_0_lim[0] < f_0_test
    assert f_0_lim[1] > f_0_test
    assert gamma_lim[0] < gamma_test
    assert gamma_lim[1] > gamma_test
    assert np.shape(f_0_mesh) == np.shape(gamma_mesh)


def test_get_ul_f_0():
    '''
    Test if the calculation of f_0 from the implicit condition
    lambda_s = lambda_limi is correct.
    This also tests effective_area_averaged_flux() and power_law()
    '''
    gamma_test = -2.6
    a_eff = get_a_eff_list()[2]  # Veritas V5 lowZd

    f_0_calc = gls.get_ul_f_0(
        t_obs=7.*3600.,
        l_lim=11.3,
        a_eff_interpol=a_eff,
        e_0=1.,
        gamma=gamma_test
        )

    assert f_0_calc < 2e-13
    assert f_0_calc > 1e-13


def test_sensitive_energy():
    '''
    Test if the calculation of the sensitive energy
    makes sense.
    '''
    gamma_test = -2.6
    a_eff = get_a_eff_list()[2]  # Veritas V5 lowZd

    sensitive_e = gls.sensitive_energy(gamma_test, a_eff)

    assert sensitive_e < 1.
    assert sensitive_e > 0.1


def test_integral_spectral_exclusion_zone():
    '''
    Test the function for calculating the integral spectral exclusion zone
    '''
    energy_test = 1.2  # TeV
    l_lim_test = 11.3
    t_obs_test = 7.*3600.  # in s
    a_eff = get_a_eff_list()[2]  # Veritas V5 lowZd

    f_0_result, gamma_result = gls.integral_spectral_exclusion_zone_parameters(
        energy_test, l_lim_test, a_eff, t_obs_test)

    # test results
    assert f_0_result > 1e-14
    assert f_0_result < 1e-10
    assert gamma_result > -10
    assert gamma_result < 0.5

    # cross check that the sensitive energy for inferred gamma is actually
    # equal (to one permille) to the one calculated with the Lagrangian result
    sensitive_e = gls.sensitive_energy(gamma_result, a_eff)
    assert np.abs(sensitive_e-energy_test)/energy_test < 1e-4
