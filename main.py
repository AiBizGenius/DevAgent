from agents.github_actions_agent import GitHubActionsAgent, GitHubActionsConfig
from agents.dockerfile_agent import DockerfileAgent, DockerfileConfig
from agents.build_predictor_agent import BuildPredictorAgent, BuildPredictorConfig
from agents.code_review_agent import CodeReviewAgent, CodeReviewConfig
from agents.build_status_agent import BuildStatusAgent, BuildStatusConfig
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main orchestration function that coordinates the DevOps AI team's activities.
    
    This function manages four main tasks:
    1. Creating a GitHub Actions CI/CD pipeline
    2. Generating a Dockerfile
    3. Building and checking Docker image status
    4. Predicting build success/failure
    """
    print("🤖 DevOps AI Team Starting Up...")
    report_lines = ["# 🧐 DevOps AI Team Report\n"]

    # 1. Create GitHub Actions Pipeline
    print("\n1️⃣ GitHub Actions Agent: Creating CI/CD Pipeline...")
    gha_config = GitHubActionsConfig(
        workflow_name="CI Pipeline",
        python_version="3.13.0",
        run_tests=True,
        groq_api_endpoint=os.getenv("GROQ_API_ENDPOINT"),
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    gha_agent = GitHubActionsAgent(config=gha_config)
    pipeline = gha_agent.generate_pipeline()
    
    # Save the pipeline configuration to a YAML file
    with open(".github/workflows/CI3.yml", "w", encoding="utf-8") as f:
        f.write(pipeline)
    print("✅ CI/CD Pipeline created!")
    report_lines.append("## 🔧 Pipemaster: GitHub Actions CI/CD Pipeline\nCI/CD pipeline generated and saved to `.github/workflows/ci_pipeline.yml`.\n")

    # 2. Create Dockerfile
    print("\n2️⃣ Dockerfile Agent: Creating Dockerfile...")
    docker_config = DockerfileConfig(
        base_image="nginx:alpine",  # Using lightweight nginx image
        expose_port=80,  # Standard HTTP port
        copy_source="./html",  # Source directory for web content
        work_dir="/usr/share/nginx/html",  # Default nginx content directory
        groq_api_endpoint=os.getenv("GROQ_API_ENDPOINT"),
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    docker_agent = DockerfileAgent(config=docker_config)
    dockerfile = docker_agent.generate_dockerfile()
    
    # Save the Dockerfile
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile)
    report_lines.append("## 🐳 Dockergenius: Dockerfile Generation\nDockerfile created and saved as `Dockerfile`.\n")
    print("✅ Dockerfile created!")

    # 3. Build and Check Status
    print("\n3️⃣ Build Status Agent: Building and checking Docker image...")
    status_config = BuildStatusConfig(image_tag="myapp:latest")
    status_agent = BuildStatusAgent(config=status_config)
    
    # Attempt to build the Docker image
    print("🔨 Building Docker image...")
    import subprocess
    build_result = subprocess.run(
        ["docker", "build", "-t", "myapp:latest", "."],
        capture_output=True,  # Capture command output
        text=True  # Return string instead of bytes
    )
    
    # Verify the build status
    status = status_agent.check_build_status()
    print(f"📊 Build Status: {status}")
    report_lines.append(f"## 🔍 BuildSentinel: Docker Build Status\nBuild Status: **{status}**\n")

    # 4. Predict Build Success/Failure
    print("\n4️⃣ Build Predictor Agent: Analyzing build patterns...")
    predictor_config = BuildPredictorConfig(
        model="llama3-8b-8192",  # Using Groq's recommended model
        groq_api_endpoint=os.getenv("GROQ_API_ENDPOINT"),
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    predictor_agent = BuildPredictorAgent(config=predictor_config)
    
    # Prepare build data for analysis
    build_data = {
        "dockerfile_exists": True,  # Dockerfile was created
        "ci_pipeline_exists": True,  # CI pipeline was created
        "last_build_status": status,  # Result of the latest build
        "python_version": "3.13.0",  # Python version being used
        "dependencies_updated": True  # Dependencies are current
    }
    
    # Get build prediction
    prediction = predictor_agent.predict_build_failure(build_data)
    print(f"🔮 Build Prediction: {prediction}")
    report_lines.append(f"## 🔮 Foresight: Build Failure Prediction\nPrediction: **{prediction}**\n")
    # 🧑‍💻 Agent 5: Codemage (Code Reviewer)
    print("🧑‍💻 Codemage is reviewing the sample Python file...")
    code_review_config = CodeReviewConfig(
        groq_api_endpoint=os.getenv("GROQ_API_ENDPOINT"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-8b-8192",
        github_token=os.getenv("GITHUB_TOKEN"),
        repo_name="sample-user/sample-repo",  # Fake repo name for standalone run
        pull_request_number=1                # Not used in this offline test
    )

    # Replace CodeReviewAgent methods for offline usage
    codemage = CodeReviewAgent(config=code_review_config)
    sample_code_path = "html/aignite.html"

    with open(sample_code_path, "r") as f:
        sample_code = f.read()

    from models.groq_models import CodeReviewRequest
    request = CodeReviewRequest(
        file_name="aignite.html",
        file_content=sample_code,
        diff="Initial sample file."
    )
    review = codemage.groq_client.send_code_review_request(
        model_id=codemage.config.model,
        code_review_request=request
    )
    issues = (
        "\n".join([
            f"- ❌ **[{i.get('type', 'Unknown')}]** at line(s) `{', '.join(map(str, i.get('line_numbers', [])))}`:\n\n"
            f"  ```\n  {i.get('description', '')}\n  ```"
            for i in review.issues
        ]) if review.issues else "**✅ No issues found.**"
    )

    suggestions = (
        "\n".join([
            f"- 💡 **Suggestion** at line(s) `{', '.join(map(str, s.get('location', [])))}`:\n\n"
            f"  ```\n  {s.get('suggestion', '')}\n  ```"
            if isinstance(s, dict)
            else f"- 💡\n  ```\n  {s}\n  ```"
            for s in review.suggestions
        ]) if review.suggestions else "**👍 No suggestions at this time.**"
    )

    report_lines.append(
        f"## 🧑‍💻 Codemage: Code Review\n"
        f"**Overall Quality**: {review.overall_quality}\n\n"
        f"**Issues:**\n\n{issues}\n\n"
        f"**Suggestions:**\n\n{suggestions}\n"
    )

    # Write final markdown report
    with open("devops_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("\n✅ DevOps AI Team report saved to `devops_report.md`")

    print("\n✨ DevOps AI Team has completed their tasks!")


if __name__ == "__main__":
    main()
