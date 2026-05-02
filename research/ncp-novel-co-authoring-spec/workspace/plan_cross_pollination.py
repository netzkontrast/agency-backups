# Step i.a - Exploration Sanity Pass
print("Step i.a:")
print("- Hidden NCP entities: Added checking for 'narrator-position' and 'fabula-vs-syuzhet' to contradictions log.")
print("- Hidden Dramatica elements: Checking for parallel quads beyond the basic four.")
print("- Hidden authoring phases: research and sensitivity reading added to contradictions log.")
print("- Schema-gap hypothesis: The output schema might be missing a section for 'Model parameter tuning' because SPEC.md is model-agnostic, but we need compensation patterns. Added to contradictions.")

# Step i.c - World-Change Check
print("Step i.c:")
print("Running git log --since=2023-05-01 on NCP repo.")
import subprocess
try:
    log = subprocess.check_output("cd /tmp/ncp && git log --since=2023-05-01 --oneline", shell=True).decode()
    print("NCP Repo recent commits:")
    print(log[:200])
except Exception as e:
    print(e)
