import os

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import json
from .models import Post
from users.models import User
from django.http import JsonResponse
import json


def home(request):
    current_user = request.user.groups.filter(name='орда').exists()
    context = {
        'posts': Post.objects.all(),
        'allow': current_user,
    }
    return render(request, 'blog/home.html', context)


def my_home(request):
    current_user = request.user.groups.filter(name='орда').exists()
    context = {
        'posts': Post.objects.filter(author_id=request.user.id),
        'allow': current_user,
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'Орда'})


def schedule(request, pk):
    posts = Post.objects.filter(id=pk)
    com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "w", encoding="utf-8")
    com_file.write(str(posts[0].content.replace("\n", "")))
    com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "r", encoding="utf-8")
    com_file.seek(0)
    commands_dict = {}
    file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "r", encoding="utf-8")
    if len(file.read()) == 0:
        file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "w", encoding="utf-8")
        num = 1
        title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
        file.write(title + "\n")
        file.write("-" * len(title) + "\n")
        for command in com_file.readlines():
            file.write(command.replace("\n", "").ljust(37) + "\n")
            commands_dict[command.replace("\n", "").strip()] = []
            if num % 2 == 0:
                file.write("-" * len(title) + "\n")
            num += 1
        file.close()

    file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "r", encoding="utf-8")
    file_count = open(f"{posts[0].title}/{posts[0].title}_туры.txt", "r", encoding="utf-8")
    count_tour = int(file_count.read())
    com_1 = []
    com2_1, com2_2 = [], []
    com3_1, com3_2, com3_3 = [], [], []
    com4_1, com4_2, com4_3, com4_4 = [], [], [], []
    com5_1, com5_2, com5_3, com5_4, com5_5 = [], [], [], [], []
    com6_1, com6_2, com6_3, com6_4, com6_5, com6_6 = [], [], [], [], [], []

    l = []
    for line in file.readlines()[2:]:
        line = line.replace("\n", "")
        if line.count('-') > 0:
            com_1.append(l)
            l = []
        else:
            l.append(line)

    file_count = open(f"{posts[0].title}/{posts[0].title}_туры.txt", "r", encoding="utf-8")
    all_tour = int(file_count.read())
    if all_tour != 1:
        file_res = open(f"{posts[0].title}/результат_{all_tour - 1}_{posts[0].title}.txt", "r", encoding="utf-8")
    else:
        file_res = open(f"{posts[0].title}/результат_{all_tour}_{posts[0].title}.txt", "r", encoding="utf-8")

    file_res.seek(0)
    com_d = {}
    for i in range(0, 10):
        com_d[i] = []
    for line in file_res.readlines():
        if len(line.replace("\n", "")) != 0:
            com = line.split(": ")[0]
            win = int(line.split(": ")[1])
            com_d[win].append(com)

    match all_tour:
        case 6:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)


            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_5.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com5_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com5_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com5_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com5_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com5_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_5_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)



            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[5]) - 1, 2):
                if com_d[5][i + 1] not in commands_dict[com_d[5][i]]:
                    com6_1.append([com_d[5][i], com_d[5][i + 1]])
                else:
                    empty_com_1.append(com_d[5][i])
                    empty_com_2.append(com_d[5][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com6_2.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com6_3.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com6_4.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com6_5.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com6_6.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_6.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            file = open(f"{posts[0].title}/{posts[0].title}_тур6.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур6.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com6_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5,
                           'tour6_1': com6_1, 'tour6_2': com6_2, 'tour6_3': com6_3, 'tour6_4': com6_4, 'tour6_5': com6_5, 'tour6_6': com6_6})
        case 5:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2


            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com5_1.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com5_2.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com5_3.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com5_4.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com5_5.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            file = open(f"{posts[0].title}/{posts[0].title}_тур5.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур5.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com5_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5})
        case 4:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p+1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p+1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p+1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com4_1.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com4_2.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com4_3.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com4_4.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            file = open(f"{posts[0].title}/{posts[0].title}_тур4.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур4.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com4_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            for i in range(0, len(com4_1)):
                if com4_1[i][0][:25].replace("\n", "").strip() not in commands_dict[com4_1[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com4_1[i][1][:25].replace("\n", "").strip()].append(com4_1[i][0][:25].replace("\n", "").strip())
                if com4_1[i][1][:25].replace("\n", "").strip() not in commands_dict[com4_1[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com4_1[i][0][:25].replace("\n", "").strip()].append(com4_1[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com4_2)):
                if com4_2[i][0][:25].replace("\n", "").strip() not in commands_dict[com4_2[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com4_2[i][1][:25].replace("\n", "").strip()].append(com4_2[i][0][:25].replace("\n", "").strip())
                if com4_2[i][1][:25].replace("\n", "").strip() not in commands_dict[com4_2[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com4_2[i][0][:25].replace("\n", "").strip()].append(com4_2[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com3_3)):
                if com4_3[i][0][:25].replace("\n", "").strip() not in commands_dict[com4_3[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com4_3[i][1][:25].replace("\n", "").strip()].append(com4_3[i][0][:25].replace("\n", "").strip())
                if com4_3[i][1][:25].replace("\n", "").strip() not in commands_dict[com4_3[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com4_3[i][0][:25].replace("\n", "").strip()].append( com4_3[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com4_4)):
                if com4_4[i][0][:25].replace("\n", "").strip() not in commands_dict[com4_4[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com4_4[i][1][:25].replace("\n", "").strip()].append(com4_4[i][0][:25].replace("\n", "").strip())
                if com4_4[i][1][:25].replace("\n", "").strip() not in commands_dict[com4_4[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com4_4[i][0][:25].replace("\n", "").strip()].append( com4_4[i][1][:25].replace("\n", "").strip())

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4})
        case 3:

            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_{all_tour - 1}_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com3_1.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com3_2.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com3_3.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com3_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com3_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com3_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            for i in range(0, len(com3_1)):
                if com3_1[i][0][:25].replace("\n", "").strip() not in commands_dict[com3_1[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com3_1[i][1][:25].replace("\n", "").strip()].append(com3_1[i][0][:25].replace("\n", "").strip())
                if com3_1[i][1][:25].replace("\n", "").strip() not in commands_dict[com3_1[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com3_1[i][0][:25].replace("\n", "").strip()].append(com3_1[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com3_2)):
                if com3_2[i][0][:25].replace("\n", "").strip() not in commands_dict[com3_2[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com3_2[i][1][:25].replace("\n", "").strip()].append(com3_2[i][0][:25].replace("\n", "").strip())
                if com3_2[i][1][:25].replace("\n", "").strip() not in commands_dict[com3_2[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com3_2[i][0][:25].replace("\n", "").strip()].append(com3_2[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com3_3)):
                if com3_3[i][0][:25].replace("\n", "").strip() not in commands_dict[com3_3[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com3_3[i][1][:25].replace("\n", "").strip()].append(com3_3[i][0][:25].replace("\n", "").strip())
                if com3_3[i][1][:25].replace("\n", "").strip() not in commands_dict[com3_3[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com3_3[i][0][:25].replace("\n", "").strip()].append( com3_3[i][1][:25].replace("\n", "").strip())

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3})
        case 2:

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i+1] not in commands_dict[com_d[1][i]]:
                    com2_1.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com2_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            # ------
            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com2_2.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])


            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com2_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 30 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com2_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com2_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                checkbox = list(request.GET.get("data"))
                game = request.GET.get("name")
                file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
                file_list = []
                i = 0

                l = len(file.readlines())
                file.seek(0)
                for line in file.readlines()[:l-1]:
                    if line.count("КОМАНДЫ") or line.count("---------------"):
                        file_list.append(line)
                    else:
                        new_line = line.replace("\n", "")
                        l1 = new_line[:len(line) // 2]
                        l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                        new_line = l1 + l2 + checkbox[i] + "\n"
                        file_list.append(new_line)
                        i += 1

                file.close()

                file = open(f"{game}/{game}_тур2.txt", "w", encoding="utf-8")
                for el in file_list:
                    file.write(el)
                file.close()

                # # init dict with commands

                file_res = open(f"{game}/результат_1_{game}.txt", "r", encoding="utf-8")
                com_dict = {}
                for line in file_res.readlines():
                    if line.count(": ") > 0:
                        com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

                # count win
                for el in file_list[1:]:
                    if el.count("-") < 5:
                        com = el[:25].strip()
                        score = el[25:].strip()
                        com_dict[com] += int(score)

                # save results from 2 tour
                res = open(f"{game}/результат_2_{game}.txt", "w", encoding="utf-8")
                for i in range(0, 10):
                    k = 0
                    for pair in com_dict.items():
                        if pair[1] == i and pair[0] != "Пустышка":
                            res.write(pair[0] + ": " + str(i) + "\n")
                            k += 1
                    if k % 2 != 0:
                        res.write("Пустышка" + ": " + str(i) + "\n")
                    res.write("\n")
                res.close()
                # new tour
                file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
                file_count.write("3")
                data = {"message": "ok"}
                return JsonResponse(data)
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)
            commands_dict["Пустышка"] = []

            for i in range(0, len(com2_1)):
                if com2_1[i][0][:25].replace("\n", "").strip() not in commands_dict[com2_1[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com2_1[i][1][:25].replace("\n", "").strip()].append(com2_1[i][0][:25].replace("\n", "").strip())
                if com2_1[i][1][:25].replace("\n", "").strip() not in commands_dict[com2_1[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com2_1[i][0][:25].replace("\n", "").strip()].append(com2_1[i][1][:25].replace("\n", "").strip())

            for i in range(0, len(com2_2)):
                if com2_2[i][0][:25].replace("\n", "").strip() not in commands_dict[com2_2[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com2_2[i][1][:25].replace("\n", "").strip()].append(com2_2[i][0][:25].replace("\n", "").strip())
                if com2_2[i][1][:25].replace("\n", "").strip() not in commands_dict[com2_2[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com2_2[i][0][:25].replace("\n", "").strip()].append(com2_2[i][1][:25].replace("\n", "").strip())


            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2})
        case 1:
            if os.path.exists(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json"):
                fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
                commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            for i in range(0, len(com_1)):
                if com_1[i][1][:25].replace("\n", "").strip() not in commands_dict[com_1[i][0][:25].replace("\n", "").strip()]:
                    commands_dict[com_1[i][0][:25].replace("\n", "").strip()].append(com_1[i][1][:25].replace("\n", "").strip())
                if com_1[i][0][:25].replace("\n", "").strip() not in commands_dict[com_1[i][1][:25].replace("\n", "").strip()]:
                    commands_dict[com_1[i][1][:25].replace("\n", "").strip()].append(com_1[i][0][:25].replace("\n", "").strip())

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': count_tour,
                           'tour1': com_1})


def save_tour_1(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        file = open(f"{game}/{game}_счёт_1.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                l1 = new_line[:len(line) // 2]
                l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                new_line = l1 + l2 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()
        file = open(f"{game}/{game}_тур1.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands
        commands_file = open(f"{game}/команды_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for com in commands_file.readlines():
            com_dict[com.replace("\n", "")] = 0

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:25].strip()
                score = el[25:].strip()
                com_dict[com] += int(score)

        # save results from 1 tour
        res = open(f"{game}/результат_1_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("2")

        data = {"message": "ok"}
        return JsonResponse(data)


def reset_1(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("1")
        file_count.close()

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            if key != "Пустышка":
                commands_dict[key] = [commands_dict[key][0]]


        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_2(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        file = open(f"{game}/{game}_счёт_2.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                l1 = new_line[:len(line) // 2]
                l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                new_line = l1 + l2 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур2.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # # init dict with commands

        file_res = open(f"{game}/результат_1_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:25].strip()
                score = el[25:].strip()
                com_dict[com] += int(score)

        # save results from 2 tour
        res = open(f"{game}/результат_2_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("3")
        data = {"message": "ok"}
        return JsonResponse(data)


def reset_2(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("2")
        file_count.close()

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = [commands_dict[key][0]]

        print(commands_dict)

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)

        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_3(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        file = open(f"{game}/{game}_счёт_3.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур3.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                l1 = new_line[:len(line) // 2]
                l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                new_line = l1 + l2 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур3.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_2_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:25].strip()
                score = el[25:].strip()
                com_dict[com] += int(score)

        # save results from 2 tour
        res = open(f"{game}/результат_3_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("4")
        data = {"message": "ok"}
        return JsonResponse(data)


def reset_3(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("3")
        file_count.close()

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:3]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_4(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        file = open(f"{game}/{game}_счёт_4.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур4.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                l1 = new_line[:len(line) // 2]
                l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                new_line = l1 + l2 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур4.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_3_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:25].strip()
                score = el[25:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_4_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("5")
        data = {"message": "ok"}
        return JsonResponse(data)


def reset_4(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("4")
        file_count.close()

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:4]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)



def save_tour_5(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        file = open(f"{game}/{game}_счёт_5.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур5.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                l1 = new_line[:len(line) // 2]
                l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                new_line = l1 + l2 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур5.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_4_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:25].strip()
                score = el[25:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_5_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("6")
        data = {"message": "ok"}
        return JsonResponse(data)


def reset_5(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("5")
        file_count.close()

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:5]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)



def new_files(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        os.mkdir(name)
        file = open(f"{name}/{name}_туры.txt", "w", encoding="utf-8")
        file.write("1")
        file.close()
        for i in range(1, 10):
            file = open(f"{name}/{name}_тур{i}.txt", "w", encoding="utf-8")
            file_res = open(f"{name}/результат_{i}_{name}.txt", "w", encoding="utf-8")
            file.close()
            file_res.close()
        data = {"message": "ok"}
        return JsonResponse(data)
