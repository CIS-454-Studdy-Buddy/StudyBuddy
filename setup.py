from setuptools import setup, find_packages
print(find_packages())

setup(
        name="StudyBuddy",
        version="1.0.1",
        description="StudyBuddy",
        long_description="StudyBuddy",
        author="Aaron Alakkadan",
        license="MIT",
        classifiers=[
                "Development Status :: 4 - Beta",
                "Intended Audience :: Developers", 
                "License :: OSI Approved :: MIT License"
        ],
        keywords="studybuddy sustudybuddy",
        packages=find_packages(exclude=("tests",)),
        # trying to add files...
        include_package_data=True,
        python_requires="~=3.9"
)




