.PHONY: update

update:
	git submodule update --init --remote
	git add clang-format clang-tidy
	git diff --cached --quiet || git commit -m "Update submodules to latest commits"
	git push
