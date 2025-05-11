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

    def get_dialogues(self, script_id):
        return self.repo.get_dialogues_by_script_id(script_id)

    def update_dialogue_mapping(self, dialogue_id, job_id, status):
        self.repo.update_dialogue_job(
            dialogue_id=dialogue_id,
            job_id=job_id,
            status=status
        )

    def create_dialogue_mapping(self, dialogue_id, job_id, status, batch_id: str):
        self.repo.create_dialogue_mapping(dialogue_id, job_id, status, batch_id)

    def get_highest_batch_id(self):
        return self.repo.get_highest_batch_id()

