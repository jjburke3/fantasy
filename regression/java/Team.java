public class Team {
	private String teamName;
	private float projScore;
	public Team(String teamName, float projScore) {
		this.teamName = teamName;
		this.projScore = projScore;
	}
	
	public String getName() {
		return this.teamName;
	}
}