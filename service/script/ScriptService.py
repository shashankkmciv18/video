from repository.ScriptRepository import ScriptRepository


class ScriptService:
    def __init__(self, repo):
        self.repo = repo

    def save_script(self, data):
        title = data['Topic']
        script_id = self.repo.create_script(title)

        seq_counter = 1
        for section_name, dialogues in data.items():
            if section_name == "Topic":
                continue

            section_id = self.repo.create_section(section_name, script_id)

            for dialogue in dialogues:
                self.repo.create_dialogue(
                    speaker=dialogue["Speaker"],
                    tone=dialogue["Tone"],
                    dialogue=dialogue["Dialogue"],
                    pause=dialogue.get("Pause", 0),
                    seq_id=seq_counter,
                    script_id=script_id,
                    section_id=section_id
                )
                seq_counter += 1

        self.repo.commit()
        return script_id
