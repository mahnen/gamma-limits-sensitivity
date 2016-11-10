from setuptools import setup

setup(
    name='gamm_limits_sensitivity',
    version='0.1',
    description='Calculate integral UL and sensitiv. for g-ray telescopes.',
    url='https://github.com/mahnen/gamma_limits_sensitivity',
    author='Max Ahnen',
    author_email='m.knoetig@gmail.com',
    licence='MIT',
    packages=[
        'gamma_limits_sensitivity'
    ],
    package_data={'gamma_limits_sensitivity': ['resources/*']},
    install_requires={
        'numpy',
        'scipy',
        'matplotlib'
    },
    tests_require=['pytest']
)
