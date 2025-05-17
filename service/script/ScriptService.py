from repository.ScriptRepository import ScriptRepository


class ScriptService:
    def __init__(self, repo):
        self.repo = repo

    def save_script(self, data, weights, prompt_id):
        title = data.get('podcast_title') or data.get('title') or "default"
        script_id = self.repo.create_script(title)

        seq_counter = 1
        for section_name, dialogues in data.items():
            if section_name.lower() in ("topic", "podcast_title"):
                continue

            section_id = self.repo.create_section(section_name, script_id)

            for dialogue in dialogues:
                if not isinstance(dialogue, dict):
                    continue
                self.repo.create_dialogue(
                    speaker=dialogue["Speaker"],
                    tone=dialogue["Tone"],
                    dialogue=dialogue["Dialogue"],
                    pause=dialogue.get("Pause", 0),
                    seq_id=seq_counter,
                    script_id=script_id,
                    section_id=section_id,
                    voice_id = weights[dialogue["Speaker"]]["weight"]
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

    def fetch_audio_entries(self, batch_id: list[str]):
        rows = self.repo.fetch_tts_op(batch_ids=batch_id)
        rows_dicts = [dict(row) for row in rows]
        return rows_dicts

