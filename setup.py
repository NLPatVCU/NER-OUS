from setuptools import setup, find_packages

def readme():
    with open('README.md') as open_file:
        return open_file.read()
        
setup(
    name='NER-OUS',
    version='0.1',
    description='Biomedical NER System',
    long_description=readme(),
    packages=find_packages(),
    url='https://github.com/NanoNLP/NER-OUS',
    author='Jeffrey Smith, Bill Cramer, and Evan French',
    author_email='smithjt7@mymail.vcu.edu',
    keywords='natural-language-processing medical-natural-language-processing machine-learning nlp-library named-entity-recognition clinical-text-processing',
    python_requires=3.6,
    dependency_links=[
        'git+https://github.com/NanoNLP/medaCy@development',
    ],
    install_requires=[
        'tensorflow>=1.09',
        'bs4',
        'pandas',
        'shlex',
        'shutil',
        'spacy==2.0.13',
        'scikit-learn>=0.20.0',
        'numpy',
        'gensim'
    ],
    include_package_data=True,
    zip_safe=False
)
    