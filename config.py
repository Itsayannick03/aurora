# Aurora - A Arch Linux update assistant
# Copyright (C) 2025 Yannick Winkler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

#Let Aurora automatically update your system when packages become critical
auto_update = True

sync_time = 1

# Thresholds for update stages
stage0_threshold = 0
normal_threshold = 20
moderate_threshold = 60
high_threshold = 120
critical_threshold = 200
atomic_threshold = 500
nuclear_threshold = 1000

should_ask_today = False
