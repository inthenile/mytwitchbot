import json
class Build:
    """Used to generate and store different Guild Wars 2 builds"""
        # checking if the class name is valid. If not, we store it as undefined
        # -- which will not be accepted for Build functions.
        # I include shorthand version for classes as well to make it easier to use the commands
    async def new_build(self, name, link,):
        """This function generates a new build, adds it into the .json file.
        If it is the first build, then it creates builds.json; and enables other functions to run."""
        try:
            with open("builds.json", "r") as f:
                builds = json.load(f)
                if name in builds.keys():
                    return f"{name} already exists. Choose another name"
                else:
                    new_build = {name: link}
                builds.update(new_build)
            with open("builds.json", "w") as f:
                json.dump(builds, f)
                f.close()
            return f"{new_build} was successfully added"
        except FileNotFoundError:
            # if builds.json does not exist, create it.
            with open("builds.json", "w") as f:
                new_build = {name: link}
                json.dump(new_build, f)
                f.close()
            return f"{new_build[name]} was successfully added."

    async def delete_build(self, name):
        """Deletes an existing build on builds.json. if such a build exists."""
        try:
            with open("builds.json", "r") as f:
                builds = json.load(f)
                for key, value in builds.items():
                    if name == key:
                        info = f"{name} was removed"
                        del builds[name]
                        break
                    if name not in builds.keys():
                        return "The build does not exist. #allbuilds to check builds."
                f.close()
            with open("builds.json", "w") as f:
                json.dump(builds, f)
                f.close()
            return info
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"


    async def update_build(self, name, link):
        """Updates an existing build on builds.json. if such a build exists."""
        try:
            with open("builds.json", "r") as f:
                builds = json.load(f)
                for key, value in builds.items():
                    if name == key:
                        builds[name] = builds[name].replace(value, link)
                        break
                    if name not in builds.keys():
                        return "No such build found"
            with open("builds.json", "w") as f:
                json.dump(builds, f)
                f.close()
            return f"{name} was successfully updated."
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"

    async def show_build(self, name):
        """Reads from builds.json to show the value of the name, if such a build exists. Else, nothing is returned"""
        try:
            with open("builds.json", "r") as f:
                builds = json.load(f)
            for key, value in builds.items():
                if key == name:
                    return f"Here is the link to the {key} build: {value}"
            f.close()
            return f"There is no such build. Check #allbuilds to see the list of builds."
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"

    async def currently_available_builds(self):
        """a quick reminder to let users know what commands they can use based on the available builds"""
        try:
            builds = []
            with open("builds.json", "r") as f:
                build_data = json.load(f)
                for key, value in build_data.items():
                    builds.append(key)
                return f"Current builds: {builds} Use #build and type any of these names to see the corresponding build."
        except FileNotFoundError:
            return "No builds saved"


build = Build()