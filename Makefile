.PHONY: help commit push sync status

help:
	@echo "Available commands:"
	@echo "  make status       - Show git status"
	@echo "  make commit MSG=\"...\" - Add all changes and commit with message"
	@echo "  make push         - Push changes to current branch"
	@echo "  make sync         - Pull latest changes and push local changes"

status:
	git status

commit:
	@if [ -z "$(MSG)" ]; then echo "Error: MSG is required. Use 'make commit MSG=\"your message\"'"; exit 1; fi
	git add .
	git commit -m "$(MSG)"

push:
	git push origin HEAD

sync:
	git pull origin main --rebase
	git push origin HEAD
