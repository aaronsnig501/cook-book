# Cook Book

- [Cook Book](#cook-book)
  - [Purpose](#purpose)
  - [UX](#ux)
    - [User Stories](#user-stories)
      - [First time users](#first-time-users)
      - [Returning users](#returning-users)
      - [Site Owner](#site-owner)
    - [Design](#design)
      - [Colour](#colour)
  - [Features](#features)
    - [Authentication & Authorization](#authentication--authorization)
    - [Recipes](#recipes)
  - [Database](#database)
    - [Database Choice](#database-choice)
    - [Database structure](#database-structure)

## Purpose

My wife & I love cooking and are always sharing recipes of recipes that we'd love to cook together. The purpose of this project is to allow us to be able to not just share recipes from social media, but also to be able to keep track of the recipes we like and help us to search for the perfect weekend meal to cook.

## UX

### User Stories

#### First time users

- As a first time user I want to get an understanding of who this site is for and how it can help me
- As a first time user I want to be able to browse the site to get an idea of what it has to offer
- As a first time user I want to get access to recipes that I want to make
- As a first time user I want to find out what benefits I receive from signing up to the site
- As a first time user I want to sign up easily

#### Returning users

- As a returning user I want to sign up easily
- As a returning user I want to create a list of recipes that I like
- As a returning user I want to vote on recipes that I like or dislike
- As a returning user I want to create my own recipes
- As a returning user I want to see how many people viewed and liked my recipes
- As a returning user I want to edit recipes if they contain any textual issues
- As a returning user I want to have the option of deleting recipes
- As a returning user I want to edit my user profile
- As a returning user I want to share recipes

#### Site Owner

- As the site owner I want to have a community of users that enjoy sharing recipes
- As the site owner I want to have a collection of recipes that I can make myself

### Design

#### Colour

The purpose of this site is to showcase food and how it looks. Food can have many different colours and appearances so the colours used within the site will be neutral whites and grays to allow the images of food to stand out.

## Features

### Authentication & Authorization

- A user can create an account
- A user can log in
- A user can logout
- A user can manage their profile

### Recipes

- A user can search for recipes
- A user can filter results based on certain tags
- A user can view specific recipes
- A logged in user can create recipes
- A logged in user can edit/delete recipes
- A logged in user can like and dislike recipes
- A logged in user can favourite recipes

## Database

### Database Choice

I have chosen to work with MongoDB for this project. There are a number of reasons for this -

1. Mongo is easy to setup and work with and it's simple to use with Atlas
2. Everything can be done within Atlas so I don't need to go through the process of setting up projects, etc on another cloud platform like AWS or GCloud
3. Mongo is shema-less so I can make changes on the fly without worrying too much about managing migrations and therefore I can change the structure of the data even if I need to test something

The main drawback of using Mongo for this project is that I will need a relationship between the users and the recipes.

### Database structure

The main collections requried for this project will be `user` and `recipe`, an we'll have one more collection for `user_favourites` for now at least. This will look something like the following:

```
user
- first & last name
- email address
- password

recipe
- user_id
- name
- description
- image
- ingredients
- steps
- duration
- created_at
- total_views
- likes

user_favourites
- user_id
- favourited_items (array of recipe IDs)
```

For a more detailed diagram checkout the `docs/database/diagram.pdf`.
