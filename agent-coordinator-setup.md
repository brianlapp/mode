# 🎯 MCP Agent Coordinator Setup for Mode Swarm

## Overview
Setting up the MCP Agent Coordinator to manage our 4 swarm agents working on the Mode popup system email PNG generation fixes.

## Current Agents to Coordinate
1. **Font Fixer Agent** - Fixing "FONTS MISSING" errors
2. **Image Loader Agent** - Fixing campaign image display
3. **Database Persistence Agent** - Solving database reset issues  
4. **Quality Assurance Agent** - Ensuring professional polish

## Project Structure for Coordinator

```json
{
  "project": {
    "name": "Mode Email PNG Fix",
    "description": "Fix font rendering and image loading issues in email PNG generation",
    "status": "active",
    "agents": ["font-fixer", "image-loader", "db-persistence", "qa"]
  },
  "tasks": [
    {
      "id": "fix-database-persistence",
      "name": "Database Auto-Restore Implementation",
      "description": "Implement auto-restore on startup to prevent campaign data loss",
      "dependencies": [],
      "agent": "db-persistence",
      "files": [
        "popup-system/api/main.py",
        "popup-system/api/database.py",
        "popup-system/api/emergency_restore_endpoint.py"
      ]
    },
    {
      "id": "bundle-fonts",
      "name": "Font Bundling Solution",
      "description": "Bundle fonts with deployment to fix FONTS MISSING error",
      "dependencies": [],
      "agent": "font-fixer",
      "files": [
        "popup-system/api/main.py",
        "popup-system/api/assets/fonts/",
        "railway.toml"
      ]
    },
    {
      "id": "fix-image-loading",
      "name": "Campaign Image Loading",
      "description": "Fix image URLs and implement caching",
      "dependencies": ["fix-database-persistence"],
      "agent": "image-loader",
      "files": [
        "popup-system/api/routes/email.py",
        "popup-system/api/utils/image_cache.py"
      ]
    },
    {
      "id": "quality-polish",
      "name": "Final Quality Assurance",
      "description": "Ensure professional design standards",
      "dependencies": ["bundle-fonts", "fix-image-loading"],
      "agent": "qa",
      "files": [
        "popup-system/api/routes/email.py",
        "popup-system/api/test_email_generation.py"
      ]
    }
  ],
  "todos": [
    {
      "task_id": "fix-database-persistence",
      "items": [
        {
          "id": "db-1",
          "description": "Add startup auto-restore logic to main.py",
          "files": ["popup-system/api/main.py"],
          "status": "pending"
        },
        {
          "id": "db-2", 
          "description": "Remove Prizies from restoration data",
          "files": ["popup-system/api/emergency_restore_endpoint.py"],
          "status": "pending"
        },
        {
          "id": "db-3",
          "description": "Fix Railway volume configuration",
          "files": ["railway.toml"],
          "status": "pending"
        }
      ]
    },
    {
      "task_id": "bundle-fonts",
      "items": [
        {
          "id": "font-1",
          "description": "Update font loading to use bundled fonts",
          "files": ["popup-system/api/main.py"],
          "status": "pending"
        },
        {
          "id": "font-2",
          "description": "Add font diagnostic endpoint",
          "files": ["popup-system/api/main.py"],
          "status": "pending"
        }
      ]
    },
    {
      "task_id": "fix-image-loading",
      "items": [
        {
          "id": "img-1",
          "description": "Create image URL diagnostic script",
          "files": ["popup-system/api/test_image_urls.py"],
          "status": "pending"
        },
        {
          "id": "img-2",
          "description": "Implement image caching system",
          "files": ["popup-system/api/utils/image_cache.py"],
          "status": "pending"
        },
        {
          "id": "img-3",
          "description": "Update broken campaign image URLs",
          "files": ["popup-system/api/fix_broken_images.py"],
          "status": "pending"
        }
      ]
    },
    {
      "task_id": "quality-polish",
      "items": [
        {
          "id": "qa-1",
          "description": "Visual quality audit and fixes",
          "files": ["popup-system/api/routes/email.py"],
          "status": "pending"
        },
        {
          "id": "qa-2",
          "description": "Performance optimization",
          "files": ["popup-system/api/routes/email.py"],
          "status": "pending"
        },
        {
          "id": "qa-3",
          "description": "Create comprehensive test suite",
          "files": ["popup-system/api/generate_qa_test_images.py"],
          "status": "pending"
        }
      ]
    }
  ]
}
```

## File Locking Strategy

To prevent conflicts, the coordinator will enforce these rules:

### Exclusive Files (only one agent at a time):
- `popup-system/api/main.py` - Core application file
- `railway.toml` - Deployment configuration
- `popup-system/api/database.py` - Database operations

### Shared Read Files (multiple agents can read):
- All `.md` documentation files
- Test data files
- Backup files

### Agent-Specific Files (assigned to single agent):
- Font Fixer: `popup-system/api/assets/fonts/`
- Image Loader: `popup-system/api/utils/image_cache.py`
- QA: `popup-system/api/generate_qa_test_images.py`

## Dependency Graph

```
Database Persistence Agent (Priority 1)
    ├── No dependencies - can start immediately
    └── Unlocks: Image Loader Agent

Font Fixer Agent (Priority 1)  
    ├── No dependencies - can start immediately
    └── Unlocks: Quality Assurance Agent

Image Loader Agent (Priority 2)
    ├── Depends on: Database Persistence
    └── Unlocks: Quality Assurance Agent

Quality Assurance Agent (Priority 3)
    └── Depends on: Font Fixer + Image Loader
```

## Coordinator Benefits for This Project

1. **No File Conflicts**: Database agent won't conflict with Font agent editing main.py
2. **Logical Order**: Image loader waits for stable database before testing URLs
3. **Parallel Work**: Font and Database agents work simultaneously 
4. **Clear Progress**: Real-time visibility of what each agent is doing
5. **Automatic Handoffs**: When DB agent finishes, Image agent automatically starts

## Next Steps

1. Install the MCP Agent Coordinator
2. Configure it with this project structure
3. Deploy all 4 agents with coordinator instructions
4. Monitor progress through coordinator dashboard
5. Celebrate when all tasks complete! 🎉

This setup ensures our swarm agents work efficiently without stepping on each other's toes!
